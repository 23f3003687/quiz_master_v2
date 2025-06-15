from celery import Celery
from flask import Flask
from models import db
from config import Config

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=Config.CELERY_RESULT_BACKEND,
        broker=Config.CELERY_BROKER_URL,
    )
    celery.conf.update(app.config)

    # Bind Flask app context to Celery tasks
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Create Flask app and bind Celery
def create_celery():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return make_celery(app)

celery = create_celery()
