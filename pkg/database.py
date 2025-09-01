import time
import logging
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.exc import OperationalError # type: ignore
from pkg.models import db

logger = logging.getLogger(__name__)

def init_database(app):
    max_retries = 5
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.session.execute('SELECT 1')
                logger.info("Database connection successful")
                return True
        except OperationalError as e:
            if attempt == max_retries - 1:
                logger.error(f"Database connection failed after {max_retries} attempts: {e}")
                return False
            logger.warning(f"Database connection failed (attempt {attempt + 1}), retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    return False

def check_database_connection(app):
    """Check if database is accessible"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.session.execute('SELECT 1')
                logger.info("✅ Database connection successful")
                return True
        except OperationalError as e:
            logger.error(f"❌ Database connection failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return False
    return False