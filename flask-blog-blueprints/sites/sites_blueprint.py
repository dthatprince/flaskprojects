from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user

#from app import app, db, login_manager

from db import db
from posts.models import Post
from auth.models import User


sites_blueprint = Blueprint('sites',__name__, template_folder='templates')


# redirect user from login/signup page to dashboard if user is already logged in
@sites_blueprint.before_request
def redirect_logged_in_users():
    if current_user.is_authenticated and request.endpoint in ['auth/login', 'auth/signup']:
        return redirect(url_for('sites.dashboard'))


# site navigation page routes
@sites_blueprint.route("/")
def index():
    posts = Post.query.all()
    #user_posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('index.html', posts=posts)

@sites_blueprint.route("/about")
def about():
    return render_template("about.html")

@sites_blueprint.route("/contact")
def contact():
    return render_template("contact.html")


# after login
@sites_blueprint.route('/dashboard')
@login_required
def dashboard():
    user_posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('dashboard.html', username=current_user.username, posts=user_posts)