from celery_utils import celery, make_celery
import celery_beat  # optional only if you're using periodic tasks

def main():
    from app import create_app
    app = create_app()

    # ✅ Properly bind Flask config to Celery
    make_celery(app)

    # ✅ Debug to verify environment values
    print("📦 Broker URL:", app.config.get("BROKER_URL"))
    print("📦 Result Backend:", app.config.get("RESULT_BACKEND"))

    # ✅ Import tasks after config is done
    from tasks.daily_reminder import send_daily_quiz_reminders
    from tasks.monthly_report import send_monthly_reports
    import tasks.export_quiz_history

main()
