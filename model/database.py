
from flask_sqlalchemy import SQLAlchemy
from utils.singleton import Singleton

@Singleton
class DataBase:
    def __init__(self):
        self.db = None
        self.init_db()

    def init_db(self):
        if self.db is None:
            self.db = SQLAlchemy()
