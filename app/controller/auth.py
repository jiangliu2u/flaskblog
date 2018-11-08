from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app.models import Blog, User
from flask_login import login_user, current_user, fresh_login_required, logout_user
from app.form import login_form
from datetime import datetime
from bson import json_util
import json

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username=str(form.username.data)).first()
            if user is not None and user.check_password(form.password.data):
                user.authenticated = True
                user.last_login_at = datetime.utcnow()
                user.save()
                login_user(user)  # remember=True
                flash('Thanks for logging in, {}'.format(current_user.username))
                print(current_user.username)
                return redirect(url_for('main.index'))
            flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/api/reg', methods=['POST'])
def register():
    jsondata = request.get_json()

    if jsondata['username'] and jsondata['password']:
        if User.objects(username=jsondata['username']):
            return jsonify("username already exists")
        else:
            username = jsondata['username']
            password = jsondata['password']
            user = User(username=username)
            user.password = password
            user.save()
            if user.id:
                returnUser = {
                    'id': str(user.id),
                    'username': user.username,
                }
                return jsonify({"user": returnUser, "msg": "用户注册成功"})
            else:
                return jsonify('用户注册失败')

    else:
        return jsonify('请输入用户名或者密码')


@auth.route('/logout')
def logout():
    user = current_user
    if current_user.is_authenticated:
        user.authenticated = False
        user.save()
        logout_user()
        flash('You have been logged out.')
    elif not current_user.is_autheticated:
        flash('You were not logged in.')
    return redirect(url_for('main.index'))


class Auth():
    def error_handler(self, e):
        print(e)
        return "Something bad happened", 400

    def authenticate(self, username, password):
        userInfo = User.objects(username=username).first()
        userInfo.id = str(userInfo.id)  # 把用户id转化为string，ObjectId不能序列化
        if (userInfo is None):
            self.error_handler('找不到用户')
        else:
            if (userInfo.check_password(password)):
                return userInfo
            else:
                self.error_handler('密码不正确')

    def identity(self, payload):
        id = jsonify(payload['identity'])
        return User.get(id)
