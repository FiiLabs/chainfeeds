from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields
import threading
from feeds import parse_feeds_background
import feeds

api_v1 = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    api_v1,
    version="1.0",
    title="Web3 RSS Feed API",
    description="Web3 RSS Feed API",
)

ns = api.namespace("mainoutlines", description="TODO operations")

@ns.route("/")
class MainOutlineList(Resource):
    """Shows a list of main outlines"""
    def get(self):
        """List all main outlines"""
        main_outlines = []
        for main_outline_title in feeds.global_main_outlines:
            main_outlines.append({
            'index': list(feeds.global_main_outlines.keys()).index(main_outline_title),
            'title': main_outline_title,
            })
        return main_outlines



if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    threading.Thread(target=parse_feeds_background).start()
    app.run(debug=True)