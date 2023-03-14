from flask_restx import Resource, reqparse, fields
from api import api
from model.users import Users
from model.database import DataBase
from utils.utils import reply_message

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required

from utils.jwt  import revoke_token


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
    #@ns.doc(parser=parser, body=resource_fields)
    @ns.doc(parser=parser)
    #@ns.marshal_with(resource_fields, code=201, description="login success")
    @ns.response(400, "Login error")
    def post(self):
        args = parser.parse_args()
        existing_username = Users.query.filter_by(username=args["username"]).first()
        if not existing_username:
            return reply_message(400, "username does not exist", None), 400
        if existing_username.password != args["password"]:
            return reply_message(400, "password is incorrect", {"username": existing_username}), 400
        access_token = create_access_token(identity=args["username"])
        refresh_token = create_refresh_token(identity=args["username"])
        return reply_message(201, "login success", {"username": existing_username, "access_token": access_token, "refresh_token": refresh_token}), 400

@ns.route("/register")
class Register(Resource):
    """ Register an account"""
    @ns.doc(parser=parser)
    #@ns.marshal_with(resource_fields, code=201, description="login success")
    @ns.response(400, "Regsiter error")
    def post(self):
        args = parser.parse_args()
        print ("username: ", args["username"])
        print ("password: ", args["password"])
        existing_username = Users.query.filter_by(username=args["username"]).first()
        if existing_username:
            return reply_message(400, "username already exists", None), 400
        
        new_user = Users(args["username"], args["password"], args["email"])
        db.session.add(new_user)
        db.session.commit()
        return reply_message(400, "user created successfully", {"username": args["username"]}), 201


@ns.route("/logout")
class Logout(Resource):
    """ Logout an account"""
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        revoke_token(jti)
        return reply_message(201, "logout successfully", {"jti": jti}), 201

# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
# http POST :5000/refresh Authorization:"Bearer $REFRESH_TOKEN"
@ns.route("/refresh")
class Refresh(Resource):
    """ Refresh JWT token"""
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return reply_message(201, "token refresh successfully", {"access_token": access_token}), 201
    
# http GET :5000/protected Authorization:"Bearer $JWT access token"
@ns.route("/protected")
class Protected(Resource):
    """ Protected resource for jwt test"""
    @jwt_required()
    def get(self):
        return reply_message(201, "access jwt protected resource",None), 201