from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Define celery instance globally so it can be imported
celery = Celery(
    __name__,
    broker=os.getenv("broker_url"),
    backend=os.getenv("result_backend")
)

# ✅ Wrap config/app binding in a function
def make_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery
