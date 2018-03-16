from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_mongoengine import MongoEngine


mongo = MongoEngine()


class User(mongo.Document):
    username = mongo.StringField(required = True)
    password_hash = mongo.StringField(required = True)
    meta = {
        'collection':'user'
    }
    @property
    def password(self):
        raise AttributeError('NO ACCESS!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
            
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    
        
    def check_password(self , password):
        return check_password_hash(self.password, password)
    
    

class Blog(mongo.Document):
    username = mongo.StringField(required=True)
    weibo_content = mongo.StringField(required=True)
    pub_date = mongo.DateTimeField()
    meta = {
        'collection': 'weibo'
    }
