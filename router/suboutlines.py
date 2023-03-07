from flask_restx import Resource
from api import api
import feeds

ns = api.namespace("suboutlines", description="main outlines operations")

@ns.route("/")
class SubOutlineList(Resource):
    """Shows a list of sub outlines"""
    def get(self):
        """List all sub outlines"""
        for main_outline_title in feeds.global_main_outlines:
            suboutlines = feeds.global_main_outlines[main_outline_title]
            return "hello"