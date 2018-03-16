from .config import config, Config
from flask_login import LoginManager
from .controller import blog
from app.models import mongo
from app.extensions import bootstrap

login_manager = LoginManager()
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"
login_manager.session_protection = 'strong'

def create_app(config_name):
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.init_app(app)
    mongo.init_app(app)
    bootstrap.init_app(app)
    app.register_blueprint(blog.blog_blueprint)
    return app
