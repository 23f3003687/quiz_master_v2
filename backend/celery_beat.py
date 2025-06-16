from celery.schedules import crontab
from celery_utils import celery

celery.conf.beat_schedule = {
    'send-daily-reminders-every-morning': {
        'task': 'tasks.daily_reminder.send_daily_quiz_reminders',
        'schedule': crontab(hour=8, minute=0),  # 8:00 AM every day
    },
}
