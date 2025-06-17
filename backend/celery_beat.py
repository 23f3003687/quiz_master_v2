from celery.schedules import crontab
from celery_utils import celery

celery.conf.beat_schedule = {
    'send-daily-reminders-every-morning': {
        'task': 'tasks.daily_reminder.send_daily_quiz_reminders',
        'schedule': crontab(hour=8, minute=0),  # 8:00 AM every day
    },
        'send-monthly-report-on-first-day': {
        'task': 'tasks.monthly_report.send_monthly_reports',
        'schedule': crontab(hour=9, minute=0, day_of_month=1),  # 9:00 AM on 1st of every month
    },

}
