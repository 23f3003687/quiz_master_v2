import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # Celery & Redis
    broker_url = os.environ.get("broker_url", "redis://localhost:6379/0")
    result_backend = os.environ.get("result_backend", "redis://localhost:6379/0")
    # SQLite DB
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///quiz_master.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     # Email SMTP Settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "quizmasterv2@gmail.com")  
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")     