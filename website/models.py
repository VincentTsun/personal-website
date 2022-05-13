from . import db
from flask_login import UserMixin, current_user, AnonymousUserMixin
from sqlalchemy.sql import func
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, abort

#user database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)

#post database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(100), default='NA')
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"),nullable=False)

#admin home page view
class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_active and current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(403)

#admin index views
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_active and current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(403)

#anonymous users setup
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'