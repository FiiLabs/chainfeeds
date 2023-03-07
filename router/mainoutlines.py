from flask_restx import Resource
import feeds
from api import api


ns = api.namespace("mainoutlines", description="main outlines operations")

main_outlines_list = list(feeds.global_main_outlines.keys())

@ns.route("/")
class MainOutlineList(Resource):
    """Shows a list of main outlines"""
    def get(self):
        """List all main outlines"""
        main_outlines = []
        for main_outline_title in feeds.global_main_outlines:
            main_outlines.append({
            'index': main_outlines_list.index(main_outline_title),
            'title': main_outline_title,
            })
        return main_outlines
    
@ns.route("/<int:index>")
@api.doc(params={"index": "The main outline index the index returned from /mainoutlines"})
class MainOutline(Resource):
    def get(self, index):
        """Shows a list sub outlines of the specific main outline"""
        if index >= len(main_outlines_list):
            api.abort(404, "Main outline {} doesn't exist".format(index))
        main_outline_title = main_outlines_list[index]
        suboutlines = feeds.global_main_outlines[main_outline_title]
        sub_outlines = []
        for sub_outline_title in suboutlines:
            sub_outlines.append({
                'title': sub_outline_title,
                'xmlUrl': suboutlines[sub_outline_title].xmlUrl,
            })
        return sub_outlines