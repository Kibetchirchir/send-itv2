from .views import User
from flask import Blueprint
from flask_restful import Api


v1 = Blueprint('apiv1', __name__, url_prefix=("/api/v1"))
api = Api(v1)

api.add_resource(User, '/signup')

