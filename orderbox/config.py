import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql:///root:root@db/main"
    SQLALCHEMY_TRACK_MODIFICATIONS = False