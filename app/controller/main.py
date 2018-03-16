from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import Blog, User
from flask_login import login_user, current_user, fresh_login_required
from app.form import post_form
from datetime import datetime

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    diaries = Blog.objects.all().order_by('pub_date')
    return render_template('index.html', diaries=diaries)


@main_blueprint.route('/new_post', methods=['GET', 'POST'])
def new_post():
    form = post_form(request.form)
    if request.method == "POST":
        if form.validate_on_submit() and current_user.is_authenticated:
            post = Blog(content=form.content.data,
                        author=User.objects(username=current_user.username).first())
            post.save()
            flash('Created successfully.')
            return redirect(url_for('main.index'))
    return render_template("new_post.html", form=form, current_time=datetime.utcnow())
