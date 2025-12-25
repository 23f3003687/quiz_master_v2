# quiz_master_v2
This is a project that includes making of a quiz app
## Running Celery Worker (Windows)



celery -A celery_worker worker --loglevel=info --pool=solo # working

system will:

 Send daily quiz reminders automatically every day at 8:00 AM.

 Send monthly reports automatically on the 1st of each month at 9:00 AM.


 order:

1️⃣ Terminal 1: Redis Server
redis-server

2️⃣ Terminal 2: Start Flask App
flask run

3️⃣ Terminal 3: Start Celery Worker
celery -A celery_worker.celery worker --loglevel=info --pool=solo

✅ You’ll see tasks getting received and processed.

4️⃣ Terminal 4: Start Celery Beat
celery -A celery_worker.celery beat --loglevel=info


send_daily_quiz_reminders.delay() is manual triggering of the task.
 use this in 2 cases:

Testing  ####FOR TESTING ONLY NOT DAILY

 to manually trigger the task outside the schedule

cd backend
flask shell

>>> from tasks.daily_reminder import send_daily_quiz_reminders
>>> send_daily_quiz_reminders.delay()
(for the daily reminder send to the mail of users)

>>>from tasks.monthly_report import send_monthly_reports
>>>send_monthly_reports.delay()
(for the monthly_report showing to mail instantly)
>>>
>>>Made by Nitya Sharma ,2025


