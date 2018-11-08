from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify
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


# @auth.route('/reg', methods=['GET', 'POST'])
# def register():
#     form = reg_form(request.form)
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             new_user = User(username=form.username.data)
#             new_user.password = form.password.data
#             print(new_user.password_hash)
#             new_user.save()
#             return redirect(url_for("main.index"))
#
#     return render_template('register.html', form=form)


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
        print(1)
        userInfo =User.objects(username=username).first()
        if (userInfo is None):
            self.error_handler('找不到用户')
        else:
            if (userInfo.check_password(password)):
                # User.update()
                print(2)
                return userInfo
            else:
                self.error_handler('密码不正确')

    def identity(self, payload):
        print(3)
        id = jsonify(payload['identity'])
        return User.get(id)