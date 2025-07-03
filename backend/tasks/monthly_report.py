# tasks/monthly_report.py
from celery_utils import celery
from models import User
from utils.csv_helper import generate_user_csv
from utils.email_helper import send_email
from datetime import date
from app import create_app

app = create_app()

@celery.task
def send_monthly_reports():
    print("📊 Sending monthly quiz performance reports...")

    users = User.query.all()
    for user in users:
        csv_path = generate_user_csv(user.user_id)
        subject = "📈 Your Monthly Quiz Report"
        body = f"Hi {user.full_name},\n\nFind attached your quiz performance report for the past month.\n\n– QuizMaster Team"
        
        send_email(user.email, subject, body, attachment_path=csv_path)
        print(f"📤 Monthly report sent to: {user.email}")
