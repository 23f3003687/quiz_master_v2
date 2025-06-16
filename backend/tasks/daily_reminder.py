from celery_utils import celery
from models import db, User, Quiz, Score
from utils.email_helper import send_email
from datetime import date
from sqlalchemy import func

@celery.task
def send_daily_quiz_reminders():
    print("🔁 Sending daily quiz reminders...")

    # Get all users who have not taken a quiz today
    today = date.today()
    
    users = User.query.all()
    for user in users:
        # Check if the user has attempted any quiz today
        attempted_today = (
            db.session.query(Score)
            .filter(Score.user_id == user.user_id, func.date(Score.timestamp) == today)
            .first()
        )

        if not attempted_today:
            subject = "📅 Daily Reminder: Attempt a Quiz Today!"
            body = f"Hi {user.name},\n\nDon't forget to take your daily quiz today on QuizMaster!\n\nGood luck!\n\n– QuizMaster Team"
            send_email(user.email, subject, body)
            print(f"📤 Reminder sent to: {user.email}")
