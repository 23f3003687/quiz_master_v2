# quiz_master_v2
This is a project that includes making of a quiz app
## Running Celery Worker (Windows)

Because of multiprocessing issues on Windows, run Celery like this:

```bash

celery -A celery_worker worker --loglevel=info --pool=solo # working

Your system will:

🔔 Send daily quiz reminders automatically every day at 8:00 AM.

📈 Send monthly reports automatically on the 1st of each month at 9:00 AM.

🧪 During Viva:
Show live in this order:

1️⃣ Terminal 1: Redis Server
redis-server

2️⃣ Terminal 2: Start Flask App
flask run

3️⃣ Terminal 3: Start Celery Worker
celery -A celery_worker.celery worker --loglevel=info --pool=solo

✅ You’ll see tasks getting received and processed.

4️⃣ Terminal 4: Start Celery Beat
celery -A celery_worker.celery beat --loglevel=info

Sir/Ma'am, the Celery worker and beat must run alongside Redis and Flask to trigger automated tasks. Once started, tasks like sending daily reminders and monthly reports are handled on schedule via Celery Beat.
For the viva, I can demonstrate sending a reminder or report manually through a test route, and the worker output will show that it's working live.

send_daily_quiz_reminders.delay() is manual triggering of the task.
You only use this in 2 cases:

🧪 Testing (e.g., for viva or debugging) ####FOR TESTING ONLY NOT DAILY

🛠️ You want to manually trigger the task outside the schedule

cd backend
flask shell

>>> from tasks.daily_reminder import send_daily_quiz_reminders
>>> send_daily_quiz_reminders.delay()
(for the daily reminder send to the mail of users)

>>>from tasks.monthly_report import send_monthly_reports
>>>send_monthly_reports.delay()
(for the monthly_report showing to mail instantly)

 every time you restart your system, you must:

Start Redis server (redis-server)

Start Flask app (flask run)

Start Celery worker (celery -A celery_worker.celery worker --loglevel=info --pool=solo)

Start Celery beat (celery -A celery_worker.celery beat --loglevel=info)

But you do NOT need to run flask shell and .delay() manually—those were just for testing.

For Milestone 10, Redis was configured with Flask-Caching to optimize expensive GET endpoints. We used @cache.cached decorators with appropriate TTLs and custom key logic where necessary (e.g., per-user dashboards). This approach enhanced performance and mitigated unnecessary DB load.”