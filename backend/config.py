import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # Celery & Redis
    BROKER_URL = os.environ.get("  ")
    RESULT_BACKEND = os.environ.get(" ")
    # SQLite DB
    SQLALCHEMY_DATABASE_URI = os.environ.get(" ")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     # Email SMTP Settings
    MAIL_SERVER = os.environ.get(" ")
    MAIL_PORT = int(os.environ.get( ))
    MAIL_USERNAME = os.environ.get(" ")  
    MAIL_PASSWORD = os.environ.get(" ")     
    # Secret Keys
    SECRET_KEY = os.environ.get(" ")
    JWT_SECRET_KEY = os.environ.get(" ")
