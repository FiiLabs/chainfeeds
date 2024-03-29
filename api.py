from flask import Blueprint
from flask_restx import Api

api_v1 = Blueprint("api", __name__, url_prefix="/api")

authorizations = {
    "JWT": {
        "type": "JWT",
        "in": "header",
        "name": "Authorization",
    }
}

api = Api(
    api_v1,
    version="1.0",
    title="Web3 RSS Feed API",
    description="Web3 RSS Feed API",
    authorizations=authorizations,
)