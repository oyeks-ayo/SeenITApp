# import os
# from flask import Flask
# from flask_wtf import CSRFProtect # type: ignore
# from flask_migrate import Migrate # type: ignore
# from dotenv import load_dotenv # type: ignore
# from pkg.config import Appconfig


# csrf = CSRFProtect()

# def create_app():
#     from pkg import forms, user_routes, admin_routes, dbroutes
#     from pkg.models import db

#     load_dotenv()  # Load environment variables from .env file
#     app = Flask(__name__,instance_relative_config=True) 
#     app.config.from_object(Appconfig) #TO MAKE THE CONFIG ITEMS CREATED IN PKG/CONFIG.PY AVAILABLE
#     app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") # Load SECRET_KEY from environment variable
#     app.config.from_pyfile('config.py', silent=True)

#     db.init_app(app)
#     csrf.init_app(app)
#     migrate = Migrate(app,db)

#     return app

# app = create_app()

# In your main app file
# pkg/__init__.py
# pkg/__init__.py
import os
import logging
from flask import Flask, jsonify
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv
from .config import Appconfig

csrf = CSRFProtect()

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Appconfig)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config.from_pyfile('config.py', silent=True)
    
    # Configure logging
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

    # Initialize extensions
    from .models import db
    db.init_app(app)
    csrf.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    from .user_routes import user_bp
    from .admin_routes import admin_bp
    from .db_routes import db_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(db_bp)

    # Add health check endpoint
    @app.route('/health')
    def health_check():
        try:
            # Simple test without database
            return jsonify({
                'status': 'ok',
                'message': 'App is running (database status unknown)'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    # Add database test endpoint
    @app.route('/test-db')
    def test_db():
        try:
            # Try a simple database operation
            result = db.session.execute('SELECT 1')
            return jsonify({
                'status': 'connected',
                'message': 'Database is accessible'
            })
        except Exception as e:
            return jsonify({
                'status': 'disconnected',
                'message': f'Database error: {str(e)}'
            }), 500

    return app

app = create_app()
# REMOVE THESE IMPORTS - they cause circular imports
# from pkg import forms, user_routes, admin_routes, dbroutes