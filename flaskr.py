import os
from flask_pymongo import PyMongo
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from pw_encrypt import encrypt_password, validate_password

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.DEBUG = True
app.config.update(
    MONGO_URI='mongodb://localhost:27017/flask',
)
mongo = PyMongo(app)


@app.route('/')
def index():
    diary = mongo.db.blog.find()
    return render_template('index.html', diaries=diary)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    return 'regPage'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usera = mongo.db.user.find({'username': request.form['username']})[0]
        print(usera, 'hahahah')
        if usera:
            if validate_password(request.form['password'], usera['password']):
                session['logged_in'] = True
                print('logged')
                flash('You were logged in')
                return redirect(url_for('index'))
            else:
                error = 'Invalid password'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    return 'logout'


if __name__ == "__main__":
    app.run()
