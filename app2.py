from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields
import threading
from feeds import parse_feeds_background
from api import api_v1
from router.mainoutlines import *
from db import DataBase
import db

def start_feeds_parser():
    threading.Thread(target=parse_feeds_background).start()

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    start_feeds_parser()
    db.db_instance = DataBase(app)
    app.run(debug=True)