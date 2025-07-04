import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # Celery & Redis
    BROKER_URL = os.environ.get("BROKER_URL", "redis://localhost:6379/0")
    RESULT_BACKEND = os.environ.get("RESULT_BACKEND", "redis://localhost:6379/0")
    # SQLite DB
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///quiz_master.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     # Email SMTP Settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "quizmasterv2@gmail.com")  
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")     
    # Secret Keys
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
