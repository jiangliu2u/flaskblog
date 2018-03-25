from .config import config, Config
from flask_login import LoginManager
from .controller import auth, main, post, article
from .controller import create_admin
from app.models import mongo
from app.extensions import bootstrap, moment

login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
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
    moment.init_app(app)
    create_admin(app)
    app.register_blueprint(auth.auth)
    app.register_blueprint(main.main)
    app.register_blueprint(post.post_main)
    app.register_blueprint(article.article_main)
    return app


@login_manager.user_loader
def load_user(username):
    from app.models import User
    return User.objects(username=str(username)).first()
