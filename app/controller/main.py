from flask import Blueprint, render_template
from app.models import Article, Blog
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)


@main.route('/')
def index():
    posts = Blog.objects.all()
    for i in posts:
        if i.post_id == '' or i.post_id is None:
            i.update(post_id=generate_password_hash(i.content))

        if i.author_name == '' or i.author_name is None:
            i.update(author_name=i.author.username)
    articles = Article.objects.all().order_by('-create_time')
    return render_template('article/article_view.html', articles=articles)
