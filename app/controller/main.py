from flask import Blueprint, render_template
from app.models import Article

main = Blueprint('main', __name__)


@main.route('/')
def index():
    articles = Article.objects.all().order_by('-create_time')
    return render_template('article/article_view.html', articles=articles)
