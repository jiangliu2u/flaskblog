from flask import Blueprint, render_template
from app.models import Blog

blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/', methods=['GET'])
def index():
    diaries = Blog.objects.all()
    return render_template('index.html', diaries=diaries)
