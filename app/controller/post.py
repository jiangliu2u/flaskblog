from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import Blog, User
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from app.form import post_form
from datetime import datetime

post_main = Blueprint('post_main', __name__)


@post_main.route('/post_view')
@login_required
def post_view():
    posts = Blog.objects.all().order_by('-create_time')
    for i in posts:
        if i.post_id == '':
            i.update(post_id=generate_password_hash(i.content))
    for i in posts:
        if i.author_name == '':
            i.update(author_name=i.author.username)
    return render_template('post/index.html', diaries=posts)


@post_main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = post_form(request.form)
    if request.method == "POST":
        if form.validate_on_submit() and current_user.is_authenticated:
            post = Blog(content=form.content.data,
                        author=User.objects(username=current_user.username).first(), author_name=current_user.username,
                        create_time=datetime.utcnow())
            post.save()
            flash('Created successfully.')
            return redirect(url_for('main.index'))
    return render_template("post/new_post.html", form=form)
