
import csv
import os
from datetime import datetime
from models import db, Score, Quiz
from sqlalchemy import extract

def generate_user_csv(user_id):
    # Folder to store CSVs
    folder = "temp_reports"
    os.makedirs(folder, exist_ok=True)

    # File path: temp_reports/user_123_report.csv
    filename = f"user_{user_id}_report.csv"
    filepath = os.path.join(folder, filename)

    # Get current month and year
    now = datetime.now()
    month = now.month
    year = now.year

    # Fetch scores for this user in current month
    scores = (
        db.session.query(Score, Quiz)
        .join(Quiz, Quiz.quiz_id == Score.quiz_id)
        .filter(Score.user_id == user_id)
        .filter(extract('month', Score.time_stamp_of_attempt) == month)
        .filter(extract('year', Score.time_stamp_of_attempt) == year)
        .all()
    )

    # Write to CSV
    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Quiz Name", "Score", "Date"])

        for score, quiz in scores:
            writer.writerow([quiz.name, score.total_score, score.time_stamp_of_attempt.strftime("%Y-%m-%d")])

    return filepath
