from flask import  Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from db import db

from auth.forms import SignupForm, LoginForm
from auth.models import User

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')


# redirect user from login/signup page to dashboard if user is already logged in
@auth_blueprint.before_request
def redirect_logged_in_users():
    if current_user.is_authenticated and request.endpoint in ['auth.login', 'auth.signup']:
        return redirect(url_for('sites.dashboard'))



# signup
@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists!', 'danger')
            return redirect(url_for('auth.signup'))
        
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html', form=form)

# login
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('sites.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html', form=form)

# logout
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

