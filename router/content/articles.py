from flask_restx import Resource, reqparse, fields
from api import api

ns = api.namespace("content", description="Content Operations")

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True, help="The title of the article", location="json")
parser.add_argument("content", type=str, required=True, help="The content of the article", location="json")

resource_fields = api.model("Article", {
    'title': fields.String(required=True, description="The title of the article"),
    'content': fields.String(required=True, description="The content of the article"),
})

@ns.route("/article")
class Article(Resource):
    """Publish a new article from user"""
    @ns.doc(parser=parser, body=resource_fields)
    @ns.marshal_with(resource_fields, code=201, description="artcile created")
    @ns.response(400, "Validation error")
    def post(self):
        args = parser.parse_args()
        print ("title: ", args["title"])
        print ("content: ", args["content"])
        return args, 201
        

