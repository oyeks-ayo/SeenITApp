import os

class Appconfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", 'fallback_secret_key')
    
    # Get the DATABASE_URL from Railway
    db_url = os.getenv("DATABASE_URL")
    
    # Convert MySQL URL for SQLAlchemy
    if db_url:
        if db_url.startswith('mysql://'):
            # Use PyMySQL driver (most reliable for deployment)
            db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
    else:
        # Fallback for local development
        db_url = 'mysql+pymysql://username:password@localhost/your_database'
    
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800,
        'pool_pre_ping': True
    }