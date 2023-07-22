from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.secret_key = "this is the secret key for the app"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # Login manager initializing and defining user_loader function to return the active user
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(int(id))

    # Loading and registering Routes that are created in different files
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")
    return app


def create_database(app):
    if not path.exists('/website' + DB_NAME):
        with app.app_context():
            db.create_all(app=app)
        print("Database created Successfully")
