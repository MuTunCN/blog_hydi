import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py
# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SEND_FILE_MAX_AGE_DEFAULT=0,
    DATABASE=os.path.join(app.root_path, 'blog_hydi.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    # SQLALCHEMY_DATABASE_URI='sqlite:////blog.hydi.db'
))
app.config.from_envvar('BLOG_HYDI_SETTINGS', silent=True)



def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.route("/")
def index():
    db = get_db()
    cur = db.execute("SELECT * FROM entries")
    entries = cur.fetchone()
    return render_template("index.html", entries=entries)


@app.route('/p/<id>')
def post(id):

    return render_template("edit.html", id=id)


@app.route('/e/a', methods=['post', 'get'])
def add():
    if not request.method == 'get':
        return render_template("edit.html")
    else:
        title = request.form("title")
        content = request.form("content")
        category = request.form("category")
        tags = request.form("tags")
        db = get_db()
        cur = db.cursor()
