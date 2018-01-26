import os
import pymongo
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent = True)


def connect_db():
    """Connects to the specific database."""
    connection = pymongo.MongoClient('127.0.0.1:27017')
    return connection


@app.route('/')
def index():
    cn = connect_db()
    diary = cn.flask.blog.find()
    return render_template('index.html', diaries=diary)


if __name__ == "__main__":
    app.run()
