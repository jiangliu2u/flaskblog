from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_mongoengine import MongoEngine

mongo = MongoEngine()


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # self.id = self.get_id()

    @property
    def password(self):
        # raise AttributeError('password is not a readable attribute')
        return self._password

    @password.setter
    def password(self, value):
        """save user name, id and password hash to json file"""
        self._password = generate_password_hash(value)

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password, password)

    def save(self):
        info = {'username': self.username, "password": self.password}
        self.db.insert(info)

    @classmethod
    def find_user_by_username(self, username):
        return self.db.find_one({"username": username})


class Blog(mongo.Document):
    username = mongo.StringField(required=True)
    weibo_content = mongo.StringField(required=True)
    pub_date = mongo.DateTimeField()
    meta = {
        'collection': 'weibo'
    }
