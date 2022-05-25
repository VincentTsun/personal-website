from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dotenv import load_dotenv


db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['SECRET_KEY'] = getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Post, MyModelView, MyAdminIndexView
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    admin = Admin(app, index_view=MyAdminIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Post, db.session))

    return app

