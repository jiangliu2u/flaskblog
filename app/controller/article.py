from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify
from app.models import User, Article
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from app.form import article_form
from datetime import datetime

article_main = Blueprint('article_main', __name__)


@article_main.route('/new_article', methods=['GET', 'POST'])
@login_required
def new_article():
    form = article_form(request.form)
    if request.method == "POST":
        if form.validate_on_submit() and current_user.is_authenticated:
            article = Article(content=form.content.data,
                              author=User.objects(username=current_user.username).first(),
                              author_name=current_user.username, title=form.title.data, create_time=datetime.utcnow())
            article.save()
            flash('Created successfully.')
            return redirect(url_for('main.index'))
    return render_template("article/new_article.html", form=form)


@article_main.route('/article/<string:article_id>', methods=['GET'])
def article_detail(article_id=''):
    article = Article.objects(id=article_id).first()
    return render_template('article/article_detail.html', article=article)

@article_main.route('/article/api/all', methods=['GET'])
def api_all():
    articles = Article.objects.all()
    return jsonify(articles)
