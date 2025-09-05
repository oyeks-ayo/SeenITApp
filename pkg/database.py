# pkg/database.py
import time
import logging
from flask import current_app
from sqlalchemy import text
from .models import db

logger = logging.getLogger(__name__)

def wait_for_database(app, max_attempts=30, delay=2):
    """Wait for database to become available without spamming logs"""
    with app.app_context():
        for attempt in range(max_attempts):
            try:
                # Simple connection test
                db.session.execute(text('SELECT 1'))
                logger.info("Database connection successful")
                return True
            except Exception as e:
                if attempt % 5 == 0:  # Log only every 5th attempt
                    logger.warning(f"Database connection attempt {attempt + 1}/{max_attempts} failed")
                if attempt == max_attempts - 1:
                    logger.error("Failed to connect to database after all attempts")
                    raise
                time.sleep(delay)
    return False