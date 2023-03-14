from flask_restx import Resource, reqparse, fields
from model.article import Article
from model.database import DataBase
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from api import api

ns = api.namespace("content", description="Content Operations")
db = DataBase.instance().db

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
    @ns.doc(parser=parser)
    #@ns.marshal_with(resource_fields, code=201, description="artcile created")
    @ns.response(400, "Validation error")
    @jwt_required()
    def post(self):
        args = parser.parse_args()
        user = get_jwt_identity()
       
        new_article = Article(args["title"], user,  datetime.now(), args["content"])
        db.session.add(new_article)
        db.session.commit()
        return {"message": "arcicle created successfully"}, 201
        
    
@ns.route("/article/<int:id>")
class ReadArticle(Resource):
    """Shows a article"""
    def get(self, id):
        return "Hello, World!", 200