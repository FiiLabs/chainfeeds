
from model.database import DataBase

db = DataBase.instance().db
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