from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Define celery instance globally
celery = Celery(
    __name__,
    broker=os.getenv("broker_url"),
    backend=os.getenv("result_backend")
)

# ✅ Properly bind Celery with Flask context
def make_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)  # ✅ FIXED

    celery.Task = ContextTask
    return celery
