from flask_restx import Resource
import utils.feeds as feeds
from api import api


ns = api.namespace("mainoutlines", description="main outlines operations")

main_outlines_list = list(feeds.get_main_outlines_from_chain_feeds())

@ns.route("/")
class MainOutlineList(Resource):
    """Shows a list of main outlines"""
    def get(self):
        """List all main outlines"""
        main_outlines = []
        mainoutlines = feeds.get_main_outlines_from_chain_feeds()
        for main_outline_title in mainoutlines:
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
        mainoutlines = feeds.get_main_outlines_from_chain_feeds()
        suboutlines = mainoutlines[main_outline_title]
        sub_outlines = []
        for sub_outline_title in suboutlines:
            sub_outlines.append({
                'title': sub_outline_title,
                'xmlUrl': suboutlines[sub_outline_title].xmlUrl,
            })
        return sub_outlines