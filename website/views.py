from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Post
from . import db

views = Blueprint("views",__name__)

@views.route('/',methods=['GET','POST'])
def home():
    try:
        admin = User.query.filter_by(is_admin=True).first()
        posts = Post.query.filter_by(author_id=admin.id).order_by(Post.date_created.desc()).all()
    except:
        posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route('/create-post',methods=['GET','POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('post_title')
        desc = request.form.get('post_desc')
        post = request.form.get('post')

        if not post:
            flash('Please enter at least one character.', category='error')
        else:
            new_post = Post(title=title, description=desc, text=post, author_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post published!', category='success')
    return render_template("create_post.html", user=current_user)

@views.route('/edit-post/<id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    form = Post()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author_id:
        flash('You do not have permission to edit this post.', category='error')
    else:
        if request.method == 'GET':
            form.title = post.title
            form.description = post.description
            form.text = post.text
            form.id = post.id
            return render_template('edit_post.html', user=current_user, post=form)
        
        elif request.method == 'POST':
            post.title = request.form.get('post_title')
            post.description = request.form.get('post_desc')
            post.text = request.form.get('post')
            
            db.session.add(post)
            db.session.commit()
            flash('Post edited.', category='success')
            return redirect(url_for('views.post', id=post.id))



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

@views.route("/portfolio")
def portfolio():
    admin = User.query.filter_by(is_admin=True).first()
    posts = Post.query.filter_by(author_id=admin.id).order_by(Post.date_created.desc()).all()
    return render_template("portfolio.html", user=current_user, posts=posts)

@views.route("/about")
def about():
    return render_template("about.html", user=current_user)

@views.route("/post/<int:id>")
def post(id):
    post = Post.query.get(id)
    return render_template("post.html", user=current_user, post=post)