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

import os
import logging
from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv
from pkg.config import Appconfig

csrf = CSRFProtect()

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Appconfig)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config.from_pyfile('config.py', silent=True)
    
    # Add SQLAlchemy connection pooling configuration
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800,
        'pool_pre_ping': True
    }
    
    # Reduce SQLAlchemy logging
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)

    # Initialize extensions
    from pkg.models import db
    db.init_app(app)
    csrf.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    from pkg.user_routes import user_bp
    from pkg.admin_routes import admin_bp
    from pkg.db_routes import db_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(db_bp)

    return app

app = create_app()
# REMOVE THESE IMPORTS - they cause circular imports
# from pkg import forms, user_routes, admin_routes, dbroutes