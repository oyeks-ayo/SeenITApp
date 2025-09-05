# pkg/config.py
import os
import logging

class Appconfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", 'fallback_secret_key')
    
    # Get the DATABASE_URL from Railway
    db_url = os.getenv("DATABASE_URL")
    
    # Convert MySQL URL for SQLAlchemy
    if db_url:
        if db_url.startswith('mysql://'):
            # Use PyMySQL driver
            db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
    else:
        # Fallback for local development
        db_url = 'mysql+pymysql://username:password@localhost/your_database'
    
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CRITICAL: Add connection timeouts and better pooling
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 60,           # Increased timeout
        'pool_recycle': 1800,
        'pool_pre_ping': True,
        'connect_args': {
            'connect_timeout': 30,    # Connection timeout
            'read_timeout': 30,       # Read timeout
            'write_timeout': 30,      # Write timeout
        }
    }

# Reduce SQLAlchemy logging globally
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)