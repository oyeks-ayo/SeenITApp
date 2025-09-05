# pkg/config.py
import os
import logging

class Appconfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", 'fallback_secret_key')
    
    # Get the DATABASE_URL from Railway
    db_url = os.getenv("DATABASE_URL")
    
    # Convert to PyMySQL driver (more reliable and compatible)
    if db_url and db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
    
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # PyMySQL compatible engine options
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800,
        'pool_pre_ping': True,
        # PyMySQL doesn't need connect_args for timeouts
    }

# Reduce SQLAlchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)