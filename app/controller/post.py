from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from app.models import Blog, User, Comment
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from app.form import post_form, comment_form,pic_post_form
from datetime import datetime
import os

post_main = Blueprint('post_main', __name__)


@post_main.route('/post_view')
@login_required
def post_view():
    User.objects(username = current_user.username).first().update(last_login_at = datetime.utcnow())
    posts = Blog.objects.all().order_by('-create_time')
    for i in posts:
        if i.post_id == '':
            i.update(post_id=generate_password_hash(i.content))
    for i in posts:
        if i.author_name == '':
            i.update(author_name=i.author.username)
    return render_template('post/index.html', diaries=posts)

@post_main.route('/post/<string:post_id>', methods=['GET', 'POST'])
def post_detail(post_id=''):
    post = Blog.objects(post_id=post_id).first()
    print(post, 'aaaaaaaaaaaaaaaaa')
    form = comment_form(request.form)
    if request.method == 'POST':
        comment = Comment(content=form.content.data,
                          comment_id=generate_password_hash(form.content.data),
                          author=User.objects(username=current_user.username).first(),
                          author_name=current_user.username,
                          create_time=datetime.utcnow())

        post1 = Blog.objects(post_id=post_id).first()
        post1.comments.append(comment)
        post1.save()
        return redirect(url_for('post_main.post_detail', post_id=post1.post_id))

    return render_template('post/post_detail.html', post=post, form=form)


@post_main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = pic_post_form(request.form)
    
    if request.method == "POST":
        
        if form.validate_on_submit() and current_user.is_authenticated:
            post = Blog(content=form.content.data,post_id=generate_password_hash(form.content.data),
                        author=User.objects(username=current_user.username).first(), author_name=current_user.username,
                        create_time=datetime.utcnow())
            if request.files['pic']:
                pic = request.files['pic']
                fname = pic.filename
                ALLOWED_EXTENSIONS=['png','jpg','jpeg','gif']
                UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
                if  not (os.path.isdir(os.path.join(UPLOAD_FOLDER))):
                    os.mkdir(os.path.join(UPLOAD_FOLDER))
                if  not (os.path.isdir(os.path.join(UPLOAD_FOLDER,current_user.username))):
                    os.mkdir(os.path.join(UPLOAD_FOLDER,current_user.username))
                flag = '.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
                if not flag:
                    flash('file type error')
                    return render_template("post/new_pic_post.html", form=form)
                # pic.save('{}{}\\{}'.format(UPLOAD_FOLDER,current_user.username,fname))#windows目录
                pic.save('{}{}/{}'.format(UPLOAD_FOLDER,current_user.username,fname))#linux目录
                # pic_pos = '\\static\\post_pic\\{}\\{}'.format(current_user.username,fname)#windows目录
                pic_pos = '/static/post_pic/{}/{}'.format(current_user.username,fname)#linux目录
                post.pic = pic_pos
            post.save()
            flash('Created successfully.')
            return redirect(url_for('post_main.post_view'))
    return render_template("post/new_post.html", form=form)