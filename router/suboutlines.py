from flask_restx import Resource
from api import api
import feeds

ns = api.namespace("suboutlines", description="main outlines operations")

@ns.route("/")
class SubOutlineList(Resource):
    """Shows a list of sub outlines"""
    def get(self):
        """List all sub outlines"""
        sub_outlines = []
        for main_outline_title in feeds.global_main_outlines:
            suboutlines = feeds.global_main_outlines[main_outline_title]
            for sub_outline_title in suboutlines:
                xmlUrl = suboutlines[sub_outline_title].xmlUrl
                title = suboutlines[sub_outline_title].title
                sub_outlines.append({
                    'title': title,
                    'xmlUrl': xmlUrl,
                })
        return sub_outlines