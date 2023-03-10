from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields
import threading
from api import api_v1
from router.mainoutlines import *
from router.suboutlines import *
import config
from flask_apscheduler import APScheduler
from datetime import datetime
from router.feeds import parse_feeds_background

app = Flask(__name__)
app.register_blueprint(api_v1)

class Config:
    """App configuration."""

    JOBS = [{"id": "job1", "func": parse_feeds_background, "trigger": "interval", "seconds": 60*60*2}]

    # SCHEDULER_JOBSTORES = {
    #     "default": SQLAlchemyJobStore(url="sqlite:///flask_context.db")
    # }

    SCHEDULER_API_ENABLED = True
 


from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config())
db = SQLAlchemy()
db.app = app
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
    
# Feeds中的各种文章内容，包括标题、正文、作者、发布时间等
class Feeds(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fromXmlUrl = db.Column(db.String(512), unique=False, nullable=False)
    title = db.Column(db.String(512), unique=False, nullable=False)
    link = db.Column(db.String(1024), unique=True, nullable=False)
    author = db.Column(db.String(128), unique=False, nullable=False)
    published = db.Column(db.String(128), unique=False, nullable=False)
    summary = db.Column(db.String(1024 * 1024 * 5), unique=False, nullable=False)
    content = db.Column(db.String(1024 * 1024 * 5), unique=False, nullable=False)

    def __init__(self, fromXmlUrl, title, link, author, published, summary, content):
        self.fromXmlUrl = fromXmlUrl
        self.title = title
        self.link = link
        self.author = author
        self.published = published
        self.summary = summary
        self.content = content

    def __repr__(self):
        return '<Title %r>' % self.title

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    for job in scheduler.get_jobs():
        job.modify(next_run_time=datetime.now())
    print("scheduler started")
    app.run(debug=True)