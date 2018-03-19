from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from mongoengine import *
from .extensions import mongo
from datetime import datetime




class User(mongo.Document, UserMixin):
    username = mongo.StringField(required=True)
    password_hash = mongo.StringField(required=True)
    authenticated = BooleanField(default=False)
    meta = {
        'collection': 'user'
    }

    @property
    def password(self):
        raise AttributeError('NO ACCESS!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Blog(mongo.Document):
    meta = {
        'collection': 'post'
    }
    # blog_id = mongo.StringField(max_length=250, required=True)  # use uuid4
    content = mongo.StringField(required=True)
    author = mongo.ReferenceField(User, reverse_delete_rule=CASCADE)
    create_time = mongo.DateTimeField(default=datetime.utcnow())

    def __repr__(self):
        return '<Post %r>' % (self.title)
