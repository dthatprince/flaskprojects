from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user

from db import db
from posts.models import Post
from posts.forms import BlogPostForm


posts_blueprint = Blueprint('posts',__name__, template_folder='templates')




@posts_blueprint.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blogpost.html', post=post)


# create post
@posts_blueprint.route('/create_post', methods=['GET', 'POST'])
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
        return redirect(url_for('sites.dashboard'))  # Redirect to dashboard after posting

    return render_template('posts/create_post.html', form=form)


# view posts
@posts_blueprint.route('/view_posts')
@login_required
def view_all_posts():
    posts = Post.query.all()
    # user_posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('posts/view_posts.html', posts=posts)
   

# update post
@posts_blueprint.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure only the author can update
    if post.author_id != current_user.id:
        flash("You are not authorized to update this post!", "danger")
        return redirect(url_for('posts.view_all_posts'))

    form = BlogPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('posts.view_all_posts'))

    # Pre-fill the form with the existing data
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.content.data = post.content

    return render_template('posts/update_post.html', form=form, post=post)



# delete post
@posts_blueprint.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure only the author can delete
    if post.author_id != current_user.id:
        flash("You are not authorized to delete this post!", "danger")
        return redirect(url_for('posts.view_all_posts'))

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for('posts.view_all_posts'))