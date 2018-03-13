from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from flask_login import UserMixin




class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        #self.id = self.get_id()
        self.db = MongoClient('127.0.0.1', 27017).flask.user

    @property
    def password(self):
        #raise AttributeError('password is not a readable attribute')
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
        info={'username':self.username,"password":self.password}
        self.db.insert(info)
    
    @staticmethod    
    def find_user_by_username(username):
        return self.db.find_one({"username":username})
