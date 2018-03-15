from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField, PasswordField, BooleanField, Form
from wtforms.validators import DataRequired, Length, EqualTo, URL
from app.models import User


class login_form(Form):
    username = StringField('username', [DataRequired(), Length(max = 32)])
    password = StringField('password', [DataRequired()])
    submit = SubmitField('Submit')
    
    def validate(self):
        check_validate = super(login_form, self).validate()
        if not check_validate:
            return False
        user = User.objects(username = self.username.data).first()
        if not user:
            self.username.errors.append("Invalid username or password")
            return False
        if not self.user.check_password(self.password.data):
            self.username.errors.append("Invalid username or password")
            return False
        
        return True
    
    
