# pkg/config.py
import os
import logging

class Appconfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", 'fallback_secret_key')
    
    # Get the DATABASE_URL from Railway
    db_url = os.getenv("DATABASE_URL")
    
    # Convert to PyMySQL driver
    if db_url and db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
    
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # TEMPORARY: Disable connection pooling to isolate the issue
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': 'NullPool'  # No connection pooling
    }

# Reduce SQLAlchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)