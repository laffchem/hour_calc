from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import flask_mail
from flask_mail import Mail
from config import APP_KEY, BOT_EMAIL, BOT_PW

db = SQLAlchemy()
DB_NAME = "users.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = APP_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Mail Server
    app.config['MAIL_SERVER'] = "smtp.mail.yahoo.com"
    app.config['MAIL_PORT']= 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = BOT_EMAIL
    app.config['MAIL_PASSWORD'] = BOT_PW
    mail = Mail(app)
    # Creates the login manager for the backend
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Hours

    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')