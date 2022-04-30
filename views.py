from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user 
from .models import User, Post
from . import db
import json

views = Blueprint("views",__name__)

@views.route('/',methods=['GET','POST'])
def home():
    admin = User.query.filter_by(username='Vincent').first()
    posts = Post.query.filter_by(author_id=admin.id).order_by(Post.date_created.desc()).all()
    return render_template("home.html", user=current_user, posts=posts )

@views.route('/create-post',methods=['GET','POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('post_title')
        post = request.form.get('post')

        if not post:
            flash('Please enter at least one character.', category='error')
        else:
            new_post = Post(title=title, text=post, author_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post published!', category='success')
    return render_template("create_post.html", user=current_user)


@views.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author_id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')
    return redirect(url_for('views.portfolio'))

@login_required
@views.route('/test2', methods=['GET','POST'])
def test2():
    return render_template("test2.html",user=current_user)


@views.route("/portfolio")
def portfolio():
    admin = User.query.filter_by(username='Vincent').first()
    posts = Post.query.filter_by(author_id=admin.id).order_by(Post.date_created.desc()).all()
    return render_template("portfolio.html", user=current_user, posts=posts)