import os
import re

class Appconfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", 'fallback_secret_key')
    
    # Get the DATABASE_URL from Railway
    db_url = os.getenv("DATABASE_URL")
    
    # Ensure it uses mysqlconnector driver
    if db_url and db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+mysqlconnector://', 1)
    
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection pool settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_timeout": 30,
        "max_overflow": 10,
        "pool_size": 5,
        "connect_args": {
            "connect_timeout": 10
        }
    }