import csv
import os
import uuid
from models import Score, Quiz, Question
from celery_utils import celery

# Generates a unique export file path
def get_export_path():
    folder = os.path.join("static", "exports")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{uuid.uuid4().hex}_quiz_history.csv")

# Collects all export data based on user_id
def get_export_data(user_id):
    scores = Score.query.filter_by(user_id=user_id).all()
    export_data = []

    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = quiz.chapter
        subject = chapter.subject

        questions = Question.query.filter_by(quiz_id=quiz.quiz_id).all()
        total_questions = len(questions)
        marks_per_question = questions[0].marks if questions else 1
        total_marks = total_questions * marks_per_question

        correct = score.correct_answers or 0
        accuracy = round((correct / total_questions) * 100, 2) if total_questions else 0

        export_data.append({
            "Quiz Name": quiz.name,
            "Subject": subject.name,
            "Chapter": chapter.name,
            "Score": score.total_score,
            "Total Marks": total_marks,
            "Correct Answers": correct,
            "Wrong Answers": score.wrong_answers or 0,
            "Accuracy (%)": f"{accuracy}%",
            "Time Taken": score.time_taken or "N/A",
            "Status": score.status or "N/A",
            "Attempted On": score.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M"),
        })

    return export_data


# Writes the data into a CSV file
def write_csv(filepath, data):
    if not data:
        return

    fieldnames = [
        "Quiz Name",
        "Subject",
        "Chapter",
        "Score",
        "Total Marks",
        "Correct Answers",
        "Wrong Answers",
        "Accuracy (%)",
        "Time Taken",
        "Status",
        "Attempted On"
    ]

    with open(filepath, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Celery task that handles the async export
@celery.task
def export_user_quiz_history(user_id):
    export_data = get_export_data(user_id)
    if not export_data:
        return None
    filepath = get_export_path()
    write_csv(filepath, export_data)
    return filepath
