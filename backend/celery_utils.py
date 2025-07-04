from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

celery = Celery(__name__, broker=os.environ.get("BROKER_URL"), backend=os.environ.get("RESULT_BACKEND"))

def make_celery(app):
    celery.conf.update(
        broker_url=app.config.get("BROKER_URL"),
        result_backend=app.config.get("RESULT_BACKEND"),
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='Asia/Kolkata',
        enable_utc=True
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
