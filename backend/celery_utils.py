from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

celery = Celery(__name__)

def make_celery(app):
    celery.conf.update(
        broker_url=app.config.get("broker_url"),
        result_backend=app.config.get("result_backend"),
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
