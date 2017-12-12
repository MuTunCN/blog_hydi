import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from datetime import datetime
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
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///blog_hydi.db'
))
app.config.from_envvar('BLOG_HYDI_SETTINGS', silent=True)
db = SQLAlchemy(app)

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                )


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    up_date = db.Column(db.DateTime)
    clicked = db.Column(db.Integer)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
                               backref=db.backref('post', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('post', lazy='dynamic'))

    def __init__(self, title, body, category, clicked, up_date=None):
        self.title = title
        self.body = body
        if up_date is None:
            up_date = datetime.utcnow()
        self.up_date = up_date
        self.category = category
        self.clicked = clicked

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<tag %r>' % self.name


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
    # db = get_db()
    # cur = db.execute("SELECT * FROM entries")
    # entries = cur.fetchone()
    entries = Post.query.order_by(Post.up_date.desc())

    return render_template("index.html", entries=entries)


@app.route('/p/<id>')
def post(id):

    return render_template("edit.html", id=id)


@app.route('/e/a', methods=['POST', 'GET'])
def add():
    if request.method == 'GET':
        return render_template("edit.html")
    else:
        title = request.form.get("title")
        content = request.form.get("content")
        category = request.form.get("category")
        tags_web = request.form.get("tags")
        tags_str = tags_web.split(",")
        c = Category(category)
        p = Post(title, content, c, 0)
        for tag in tags_str:
            t = Tag(tag)
            p.tags.append(t)
        db.session.add(p)
        db.session.commit()
        return render_template("index.html")
