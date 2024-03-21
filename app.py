from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
)
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
admin = Admin(name = "Coin Keeper", template_mode= "bootstrap3")
migrate = Migrate()
bcrypt = Bcrypt()



def create_app():
    app = Flask('Coin Keeper')
    
    app.secret_key = os.environ.get('SECRET_KEY')
    app.config['FLASK_ADMIN_SWATCH'] = 'united'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    login_manager.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    return app