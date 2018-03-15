from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_mongoengine import MongoEngine
from app.extensions import bcrypt
mongo = MongoEngine()


class User(mongo.Document):
    username = mongo.StringField(required = True)
    password = mongo.StringField(required = True)
    meta = {
        'collection':'user'
    }
    
    def __init__(self, username):
        self.username = username
        
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
        
    def check_password(self , password):
        return bcrypt.check_password_hash(self.password, password)
    
    

class Blog(mongo.Document):
    username = mongo.StringField(required=True)
    weibo_content = mongo.StringField(required=True)
    pub_date = mongo.DateTimeField()
    meta = {
        'collection': 'weibo'
    }
