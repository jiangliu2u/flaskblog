from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, TextField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from wtforms import ValidationError
from app.models import User


class login_form(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=32)])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


class reg_form(FlaskForm):
    username = StringField('用户名', [DataRequired(), Length(max=32)])
    password = PasswordField('请输入密码', [DataRequired(), Length(min=6)])
    password_rp = PasswordField('再次输入密码', [DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')

    def validate_username(self, field):
        if User.objects(username=field.data).first():
            raise ValidationError('Username already in use.')


class post_form(FlaskForm):
    content = TextAreaField('微博内容', [DataRequired()])
    submit = SubmitField('发布')

class article_form(FlaskForm):
    title = StringField('标题', [DataRequired()])
    content = TextAreaField('文章内容', [DataRequired()])
    submit = SubmitField('发布')

class admin_login_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def get_user(self):
        user = User.objects(username=self.username.data).first()
        if user is not None:
            if not check_password_hash(user.password_hash, self.password.data):
                return None
            if not user.is_admin:
                return None
            return user
        else:
            return None