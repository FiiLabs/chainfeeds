from model.database import DataBase

db = DataBase.instance().db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    articleId = db.Column(db.Integer, unique=False, nullable=False)
    username = db.Column(db.String(32), unique=False, nullable=False)
    content = db.Column(db.String(1024 * 5), unique=False, nullable=False)
    published = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, articleId, username, content, published):
        self.articleId = articleId
        self.username = username
        self.content = content
        self.published = published

    def __repr__(self):
        return '<Comment %r>' % self.content
    
class FeedComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FeedId = db.Column(db.Integer, unique=False, nullable=False)
    username = db.Column(db.String(32), unique=False, nullable=False)
    content = db.Column(db.String(1024 * 5), unique=False, nullable=False)
    published = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, FeedId, username, content, published):
        self.FeedId = FeedId
        self.username = username
        self.content = content
        self.published = published

    def __repr__(self):
        return '<Comment %r>' % self.content