import os
from flask_pymongo import PyMongo
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from login_form import login_form
import config
from models import User



app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_object('config')
app.DEBUG = True


@app.route('/')
def index():
    return render_template('index.html', diaries={})


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    user = User("jay2u","1234")
    user.save()
    return 'regPage'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form()
    error = None
#    if request.method == 'POST':
#        usera = mongo.db.user.find({'username': request.form['username']})[0]
#        print(usera, 'hahahah')
#        if usera:
#            if validate_password(request.form['password'], usera['password']):
#                session['logged_in'] = True
#                print('logged')
#                flash('You were logged in')
#                return redirect(url_for('index'))
#            else:
#                error = 'Invalid password'

    return render_template('login.html',error=error,form = form)


@app.route('/logout')
def logout():
    return 'logout'


if __name__ == "__main__":
    app.run()
