from flask_restx import Resource, reqparse, fields
from api import api
from model.user import User
from model.database import DataBase

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


ns = api.namespace("account", description="account login & logout & register")
db = DataBase.instance().db


parser = reqparse.RequestParser()
parser.add_argument("username", type=str, required=True, help="Username of account", location="json")
parser.add_argument("password", type=str, required=True, help="Password of account", location="json")
parser.add_argument("email", type=str, required=False, help="Email of account", location="json")

resource_fields = api.model("Account", {
    'username': fields.String(required=True, description="Username of account"),
    'password': fields.String(required=True, description="Password of account"),
    'email': fields.String(required=False, description="Email of account"),
})


# https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/

@ns.route("/login")
class Login(Resource):
    """ Login an account """
    @ns.doc(parser=parser, body=resource_fields)
    @ns.marshal_with(resource_fields, code=201, description="login success")
    @ns.response(400, "Login error")
    def post(self):
        args = parser.parse_args()
        print ("username: ", args["username"])
        print ("password: ", args["password"])
        existing_username = User.query.filter_by(username=args["username"]).first()
        if not existing_username:
            return {"message": "username does not exist"}, 400
        if existing_username.password != args["password"]:
            return {"message": "password is incorrect"}, 400
        access_token = create_access_token(identity=args["username"], fresh=True)
        refresh_token = create_refresh_token(identity=args["username"])
        return {"access_token": access_token, "refresh_token": refresh_token}, 201

  

@ns.route("/register")
class Register(Resource):
    """ Register an account"""
    @ns.doc(parser=parser, body=resource_fields)
    @ns.marshal_with(resource_fields, code=201, description="login success")
    @ns.response(400, "Regsiter error")
    def post(self):
        args = parser.parse_args()
        print ("username: ", args["username"])
        print ("password: ", args["password"])
        existing_username = User.query.filter_by(username=args["username"]).first()
        if existing_username:
            return {"message": "username already exists"}, 400
        

        new_user = User(args["username"], args["password"], args["email"])
        db.session.add(new_user)
        db.session.commit()
        



@ns.route("/logout")
class Logout(Resource):
    pass


@ns.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return {"access_token": access_token}, 201
    
@ns.route("/protected")
class Protected(Resource):
    @jwt_required(refresh=True)
    def get(self):
        return {"message": "protected"}, 201