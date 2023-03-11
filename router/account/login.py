from flask_restx import Resource
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from api import api
from model.user import User
from model.database import DataBase


ns = api.namespace("account", description="account login & logout & register")
db = DataBase.instance().db


# https://github.com/arpanneupane19/Python-Flask-Authentication-Tutorial/blob/main/app.py

@ns.route("/login")
class Login(Resource):
    """ Login an account """
    def get(self):
        pass
  

@ns.route("/register")
class Register(Resource):
    """ Register an account"""
    def post(self):
        existing_username = User.query.filter_by(username="test").first()
        if existing_username:
            return {"message": "username already exists"}, 400
        

        new_user = User("kk", "a121313", "aada@qq.com")
        db.session.add(new_user)
        db.session.commit()
        



@ns.route("/logout")
class Logout(Resource):
    pass