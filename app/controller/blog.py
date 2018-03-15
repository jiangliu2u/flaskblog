from flask import Blueprint, render_template, redirect, url_for
from app.models import Blog
from app.form import login_form

blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/', methods=['GET'])
def index():
    diaries = Blog.objects.all().order_by('pub_date')
    return render_template('index.html', diaries=diaries)


@blog_blueprint.route('/login', methods = ['GET','POST'])
def login():
    form = login_form()
    if form.validate():
        flash('You have been logged in.')
        return redirect(url_for('blog.index'))
    return render_template('login.html',form=form)
    
