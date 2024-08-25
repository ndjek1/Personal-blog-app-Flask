# app/__init__.py
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    @app.template_filter('format_date')
    def format_date(date_str):
        try:
            date = datetime.fromisoformat(date_str)
            return date.strftime('%B %d, %Y')  # Format as desired
        except ValueError:
            return date_str  # Return the original string if parsing fails
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    db.init_app(app)
    bcrypt.init_app(app)
    # login_manager.init_app(app)

    # from app.auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
