from model.database import DataBase

db = DataBase.instance().db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), unique=False, nullable=False)
    author = db.Column(db.String(32), unique=False, nullable=False)
    published = db.Column(db.DateTime, unique=False, nullable=False)
    content = db.Column(db.String(1024 * 1024 * 5), unique=False, nullable=False)

    def __init__(self, title, link, author, published, summary, content):
        self.title = title
        self.link = link
        self.author = author
        self.published = published
        self.content = content

    def __repr__(self):
        return '<Title %r>' % self.title