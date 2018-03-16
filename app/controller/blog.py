from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import Blog, User
from flask_login import login_user, current_user, fresh_login_required
from app.form import login_form, reg_form

blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/', methods=['GET'])
def index():
    diaries = Blog.objects.all().order_by('pub_date')
    return render_template('index.html', diaries=diaries)


@blog_blueprint.route('/login', methods = ['GET','POST'])
def login():
    form = login_form(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username=str(form.username.data)).first()
            if user is not None and user.check_password(form.password.data):
                user.authenticated = True
                user.save()
                login_user(user) # remember=True
                flash('Thanks for logging in, {}'.format(current_user.username))
                return redirect(url_for('blog.index'))
            flash('Invalid username or password.')
    return render_template('login.html', form=form)



@blog_blueprint.route('/reg', methods = ['GET', 'POST'])
def register():
    form = reg_form(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(username=form.username.data)
            new_user.password = form.password.data
            print(new_user.password_hash)
            new_user.save()
            return redirect(url_for("blog.index"))
    
    return render_template('register.html', form = form)
        
    