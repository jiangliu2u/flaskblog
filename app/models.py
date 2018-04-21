from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from mongoengine import *
from .extensions import mongo


class User(Document, UserMixin):
    username = StringField(required=True)
    password_hash = StringField(required=True)
    authenticated = BooleanField(default=False)
    isAdmin = BooleanField(default=False)
    last_login_at = DateTimeField()
    authenticated = BooleanField(default=False)
    isAdmin = BooleanField(default=False)
    meta = {
        'collection': 'user'
    }

    @property
    def password(self):
        raise AttributeError('NO ACCESS!')

    @property
    def is_admin(self):
        return self.isAdmin

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_admin(self):
        return self.isAdmin

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Comment(EmbeddedDocument):
    comment_id = StringField(max_length=250, required=True)
    content = StringField(required=True)
    author = ReferenceField(User)
    author_name = StringField(required=True)
    create_time = DateTimeField()
    def __repr__(self):
        return '<Comment %r>' % (self.content)

class Blog(Document):
    meta = {
        'collection': 'post'
    }
    content = StringField(required=True)
    pic = StringField()
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    author_name = StringField(required=True)
    create_time = DateTimeField()
    comments = EmbeddedDocumentListField('Comment')

    def __repr__(self):
        return '<Post %r>' % (self.title)


class Article(Document):
    meta = {
        'collection': 'article',
    }
    title = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    author_name = StringField(required=True)
    create_time = DateTimeField()

    def __repr__(self):
        return '<Article %r>' % (self.title)
