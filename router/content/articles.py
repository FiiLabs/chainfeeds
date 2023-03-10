from flask_restx import Resource, reqparse, fields
from api import api

ns = api.namespace("content", description="Content Operations")

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True, help="The title of the article")
parser.add_argument("content", type=str, required=True, help="The content of the article")

resource_fields = api.model("Article", {
    'title': fields.String(required=True, description="The title of the article"),
    'content': fields.String(required=True, description="The content of the article"),
})

@ns.route("/article")
class Article(Resource):
    """Publish a new article from user"""
   
    @api.doc(body=resource_fields)
    def post():
        args = parser.parse_args()
        print ("totle: ", args['title'])
        

