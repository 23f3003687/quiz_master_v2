from app import create_app
from celery_utils import celery, make_celery
import celery_beat  # This ensures beat_schedule is loaded


# Tasks must be imported after Celery setup
from tasks.daily_reminder import send_daily_quiz_reminders
from tasks.monthly_report import send_monthly_reports

flask_app = create_app()
make_celery(flask_app)  # Binds context to celery
