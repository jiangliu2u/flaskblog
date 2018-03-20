from flask_login import current_user, login_user, logout_user
from app.form import admin_login_form
from flask import redirect, url_for, request
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib.mongoengine import ModelView

# custom web form for creating user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User

class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    isAdmin = BooleanField(default=False)
    authenticated = BooleanField(default=False)

    def validate_username(self, field):
        if User.objects(username=field.data).first():
            raise ValidationError('Username already in use.')


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated and current_user.is_admin:
            return super(MyHomeView, self).index()
        return redirect(url_for('admin.login'))

    @expose('/login', methods=('GET', 'POST'))
    def login(self):
        form = admin_login_form(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                user = form.get_user()
                if user == None:
                    return redirect(url_for('admin.login'))
                elif user is not None:
                    user.authenticated = True
                    user.save()
                    login_user(user)
                    return redirect(url_for('admin.index'))
        self._template_args['form'] = form
        return super(MyHomeView, self).index()

    @expose('/logout')
    def logout_view(self):
        user = current_user
        if current_user.is_authenticated:
            user.authenticated = False
            user.save()
            logout_user()
        return redirect(url_for('admin.index'))

# custom model view when displaying
class UserView(ModelView):
    column_filters = ['username']
    column_exclude_list = ['password_hash']

    can_delete = True
    can_view_details = True
    can_create = True
    can_edit = True

    form_excluded_columns = ['password_hash']

    edit_template = 'admin/blog_edit.html'
    create_template = 'admin/blog_create.html'
    list_template = 'admin/blog_list.html'

    form = CreateUserForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class PostView(ModelView):
    can_delete = True
    can_view_details = True
    can_create = True
    can_edit = True

    column_exclude_list = ['content']

    edit_template = 'admin/blog_edit.html'
    create_template = 'admin/blog_create.html'
    list_template = 'admin/blog_list.html'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class MyView(BaseView):
    @expose('/')
    def index(self):
        return 'Hello World!'