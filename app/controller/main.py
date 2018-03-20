from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import Blog, User, Article
from flask_login import login_user, current_user, fresh_login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.form import post_form, article_form
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    posts = Blog.objects.all().order_by('-create_time')
    return render_template('index.html', diaries=posts)

@main.route('/article_view')
def article_view():
    articles = Article.objects.all().order_by('-create_time')
    return render_template('article_view.html', articles=articles)

@main.route('/new_post', methods=['GET', 'POST'])
def new_post():
    form = post_form(request.form)
    if request.method == "POST":
        if form.validate_on_submit() and current_user.is_authenticated:
            post = Blog(content=form.content.data,
                        author=User.objects(username=current_user.username).first(), author_name=current_user.username)
            post.save()
            flash('Created successfully.')
            return redirect(url_for('main.index'))
    return render_template("new_post.html", form=form, current_time=datetime.utcnow())


@main.route('/new_article', methods=['GET', 'POST'])
def new_article():
    form = article_form(request.form)
    if request.method == "POST":
        if form.validate_on_submit() and current_user.is_authenticated:
            article = Article(content=form.content.data,
                              author=User.objects(username=current_user.username).first(), author_name=current_user.username, title=form.title.data)
            article.article_id = generate_password_hash(article.title)
            article.save()
            flash('Created successfully.')
            return redirect(url_for('main.index'))
    return render_template("new_article.html", form=form, current_time=datetime.utcnow())

@main.route('/article/<string:article_id>', methods=['GET'])
def article_detail(article_id=''):
    article = Article.objects(article_id=article_id).first()
    return render_template('article_detail.html',article=article)

## TODO：1文章预览页面
## 