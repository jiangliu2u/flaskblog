from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import mongo


class User(mongo.Document, UserMixin):
    username = mongo.StringField(required=True)
    password_hash = mongo.StringField(required=True)
    authenticated = mongo.BooleanField(default=False)
    isAdmin = mongo.BooleanField(default=False)
    last_login_at = mongo.DateTimeField()
    love = mongo.ListField(mongo.StringField())
    authenticated = mongo.BooleanField(default=False)
    isAdmin = mongo.BooleanField(default=False)
    meta = {
        'collection': 'user',
        'strict': False
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




class Comment(mongo.EmbeddedDocument):
    comment_id = mongo.StringField(max_length=250, required=True)
    content = mongo.StringField(required=True)
    author = mongo.ReferenceField(User)
    author_name = mongo.StringField(required=True)
    create_time = mongo.DateTimeField()

    def __repr__(self):
        return '<Comment %r>' % (self.content)


class Blog(mongo.Document):
    meta = {
        'collection': 'post',
        'strict': False
    }
    content = mongo.StringField(required=True)
    pic = mongo.StringField()
    author = mongo.ReferenceField(User)
    author_name = mongo.StringField(required=True)
    create_time = mongo.DateTimeField()
    comments = mongo.EmbeddedDocumentListField('Comment')
    liked_by = mongo.ListField(mongo.StringField())
    def __repr__(self):
        return '<Post %r>' % (self.content)


class Article(mongo.Document):
    meta = {
        'collection': 'article',
    }
    title = mongo.StringField(required=True)
    content = mongo.StringField(required=True)
    author = mongo.ReferenceField(User)
    author_name = mongo.StringField(required=True)
    create_time = mongo.DateTimeField()

    def __repr__(self):
        return '<Article %r>' % (self.title)
