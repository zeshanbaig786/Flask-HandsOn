import os
import json
from . import app, db, login, errors
#create_app, db
from .models import User, Post, followers, PostLike
from flask import jsonify, flash, render_template, request, redirect, url_for

from flask_login import LoginManager, login_user, login_required, logout_user

from .forms import LoginForm, RegistrationForm, EmptyForm, PostForm
from werkzeug.urls import url_parse
from datetime import datetime

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#app.secret_key = 'some key'

from flask_login import current_user


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        resp = {"result": 200, "data": current_user.to_json()}
    else:
        resp = {"result": 401, "data": {"message": "user no login"}}
    return jsonify(**resp)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = current_user.followed_posts().all()
    users = User.query.all()
    form1 = EmptyForm()
    return render_template("index.html",
                           title='Home Page',
                           form=form,
                           posts=posts,
                           users=users,
                           likeForm=form1)


@app.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    form = EmptyForm()
    return render_template('index.html',
                           title='Explore',
                           posts=posts,
                           likeForm=form)


@app.route("/users/list", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])


@app.route("/user/<int:id>", methods=["GET"])
def get_book(id):
    user = User.query.get(isbn)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('create_user.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=current_user.id).order_by(
        Post.timestamp.desc()).all()
    followed = user.get_followed()
    print("followed: " + str(followed))
    followers = user.get_followers()
    print("followers: " + str(followers))
    form = EmptyForm()
    likeForm = EmptyForm()

    return render_template('user.html',
                           user=user,
                           posts=posts,
                           form=form,
                           likeForm=likeForm,
                           followed=followed,
                           followers=followers)


from app.forms import EditProfileForm


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',
                           title='Edit Profile',
                           form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/like/<int:post_id>/<action>', methods=['POST'])
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
        return '1'
    elif action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
        return '0'
    likeForm = EmptyForm()
    return render_template('_post_like_status.html',
                           post=post,
                           likeForm=likeForm)
    #return redirect(request.referrer)


@app.route('/like/<int:post_id>/viewLikes')
@login_required
def viewLikers(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('viewLikes.html', likers=post.get_likers())

@app.route('/like/<int:post_id>/get_likers', methods=['POST'])
@login_required
def get_likers_list(post_id):
    post = Post.query.get_or_404(post_id)
    print(post)
    return post.get_likers()


