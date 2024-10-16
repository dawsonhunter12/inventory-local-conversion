# app.py

import os
from flask import Flask
from config import Config
from extensions import db, login_manager
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
from whitenoise import WhiteNoise

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Set up WhiteNoise for static files
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/', prefix='static/')

    # Register Blueprints and Import Models within Application Context
    with app.app_context():
        # Import models
        from models import User

        # User loader callback for Flask-Login
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Register blueprints
        from auth_routes import auth_bp
        from inventory_routes import inventory_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(inventory_bp)

    # Configure Logging
    if not app.debug and not app.testing:
        # Ensure the logs directory exists
        if not os.path.exists('logs'):
            os.mkdir('logs')
        # Configure RotatingFileHandler
        file_handler = RotatingFileHandler('logs/inventory_app.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.INFO)
        # Set log format
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Inventory Management Application Startup')

    return app

# Expose the application instance
app = create_app()
