import os


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'hehehehehe'

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'weibo',
        'host': '127.0.0.1',
        'port': 27017
    }
    UPLOAD_FOLDER =os.getcwd()+'\\app\\static\\post_pic\\'
    

class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
