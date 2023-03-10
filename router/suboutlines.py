from flask_restx import Resource
from api import api
import utils.feeds as feeds
import utils.utils as utils

ns = api.namespace("suboutlines", description="main outlines operations")

@ns.route("/")
class SubOutlineList(Resource):
    """Shows a list of sub outlines"""
    def get(self):
        """List all sub outlines"""
        sub_outlines = []
        l = feeds.get_all_sub_outlines()
        for sub_outline in l:
            sub_outlines.append({
                'title': sub_outline.title,
                'xmlUrlBase64': utils.base64_encode(sub_outline.xmlUrl),
            })
        return sub_outlines
    

@ns.route("/<string:xmlUrlBase64>")
@api.doc(params={"xmlUrlBase64": "The sub outline xmlUrl Base64 the xmlUrl returned from /suboutlines"})
class SubOutline(Resource):
    def get(self, xmlUrlBase64):
        """Shows a list of the specific sub outline"""
        xmlUrl = utils.base64_decode(xmlUrlBase64)
        print("xmlUrl:", xmlUrl)
        if not xmlUrl in feeds.global_feeds_cache:
            suboutline = feeds.global_suboutlines_cache[xmlUrl]
            feed = feeds.parse_feed(suboutline.xmlUrl)
        else:
            feed = feeds.global_feeds_cache[xmlUrl]
        
        r_feeds = []
        for entry in feed.entries:
            link = utils.remove_prefix(entry.link, "?source=rss")
            print("entry summary:", entry.summary)
            r_feeds.append({
                'title': entry.title,
                'link': link,
                'author': entry.author,
                'published': entry.published,
                'summary': entry.summary,
                'content': entry.content,
            })
        return r_feeds