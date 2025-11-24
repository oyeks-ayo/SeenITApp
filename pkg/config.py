import os

class Appconfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", 'fallback_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", 'postgresql://postgres:0000@localhost:5432/seenITApp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
