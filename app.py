from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields
import threading
from feeds import parse_feeds_background
from api import api_v1
from router.mainoutlines import *
from router.suboutlines import *
import config

def start_feeds_parser():
    threading.Thread(target=parse_feeds_background).start()

app = Flask(__name__)
app.register_blueprint(api_v1)


from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models.user import User

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    start_feeds_parser()
    app.run(debug=True)