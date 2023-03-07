import config
from flask_sqlalchemy import SQLAlchemy

db_instance = None

class DataBase:
    __db = None
    def __new__(self, app):
        if self.__db is None:
            self.__db = self.init_db(app)
        return self.__db

    def init_db(app):
        app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlalchemy_database_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        return db


# class User(db_instance.Model):
#     id = db_instance.Column(db_instance.Integer, primary_key=True)
#     username = db_instance.Column(db_instance.String(80), unique=True, nullable=False)
#     email = db_instance.Column(db_instance.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username