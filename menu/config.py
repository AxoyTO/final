import os
from secrets import token_hex

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', token_hex(16))
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    os.environ["FLASK_ENV"] = "testing"
    TESTING = True
