from celery_utils import celery, make_celery
import celery_beat

def main():
    from app import create_app  # ✅ moved inside to avoid circular import
    app = create_app()
    
    # Bind Flask app to Celery and update config including result_backend
    make_celery(app)
    celery.conf.update(app.config)  # ✅ crucial to avoid DisabledBackend error

    # ✅ Import tasks AFTER context is ready and celery is configured
    from tasks.daily_reminder import send_daily_quiz_reminders
    from tasks.monthly_report import send_monthly_reports
    import tasks.export_quiz_history

main()
