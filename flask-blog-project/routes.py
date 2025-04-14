from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, login_manager
from models import User, Post
from forms import SignupForm, LoginForm, BlogPostForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# signup
@app.route('/signup', methods=['GET', 'POST'])
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
            return redirect(url_for('signup'))
        
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)


# after login
@app.route('/dashboard')
@login_required
def dashboard():
    user_posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('dashboard.html', username=current_user.username, posts=user_posts)

# logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



# site navigation page routes
@app.route("/")
def index():
    posts = Post.query.all()
    # user_posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('index.html', posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blogpost.html', post=post)



# create post
@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            content=form.content.data,
            author_id=current_user.id,  # Auto-filling the author ID
            author=current_user.username  # Auto-filling the username
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Your blog post has been created!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to dashboard after posting

    return render_template('create_post.html', form=form)

# view posts
@app.route('/posts')
@login_required
def view_all_posts():
    posts = Post.query.all()
    # user_posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('view_posts.html', posts=posts)
   

# update post
@app.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure only the author can update
    if post.author_id != current_user.id:
        flash("You are not authorized to update this post!", "danger")
        return redirect(url_for('view_all_posts'))

    form = BlogPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('view_all_posts'))

    # Pre-fill the form with the existing data
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.content.data = post.content

    return render_template('update_post.html', form=form, post=post)



# delete post
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure only the author can delete
    if post.author_id != current_user.id:
        flash("You are not authorized to delete this post!", "danger")
        return redirect(url_for('view_all_posts'))

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for('view_all_posts'))


# error handling
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500