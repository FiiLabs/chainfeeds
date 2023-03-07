from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields
import threading
from feeds import parse_feeds_background
from api import api_v1
from router.mainoutlines import *


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    threading.Thread(target=parse_feeds_background).start()
    app.run(debug=True)