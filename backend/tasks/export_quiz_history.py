import csv
import os
import uuid
from models import Score, Quiz, Subject
from celery_utils import celery  # ✅ CORRECT

def get_export_path():
    folder = os.path.join("static", "exports")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{uuid.uuid4().hex}_quiz_history.csv")

def get_export_data(user_id):
    scores = Score.query.filter_by(user_id=user_id).all()
    export_data = []

    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        subject = quiz.chapter.subject
        export_data.append({
            "Quiz Name": quiz.name,
            "Subject": subject.name,
            "Score": score.total_score,
            "Attempted On": score.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M"),
        })

    return export_data

def write_csv(filepath, data):
    if not data:
        return
    with open(filepath, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

@celery.task
def export_user_quiz_history(user_id):
    export_data = get_export_data(user_id)
    if not export_data:
        return None
    filepath = get_export_path()
    write_csv(filepath, export_data)
    return filepath
