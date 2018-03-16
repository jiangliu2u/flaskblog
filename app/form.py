from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from wtforms import ValidationError
from app.models import User


class login_form(FlaskForm):
    username = StringField('username', validators = [DataRequired(), Length(max = 32)])
    password = PasswordField('password', validators = [DataRequired()])
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
    

class reg_form(FlaskForm):
    username = StringField('username', [DataRequired(), Length(max = 32)])
    password = PasswordField('password', [DataRequired(),Length(min = 6)])
    password_rp = PasswordField('password_rp', [DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')
    def validate_username(self,field):
        if User.objects(username=field.data).first():
            raise ValidationError('Username already in use.')
        
    
    
    
