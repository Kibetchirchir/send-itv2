from .views import Users
from flask import Blueprint
from flask_restful import Api
from .views import Login
from .views import Parcels
from .views import GetOneParcel
from .views import CancelParcel
from .views import FetchParcelsByUsers


v1 = Blueprint('apiv1', __name__, url_prefix=("/api/v1"))
api = Api(v1)

api.add_resource(Users, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Parcels, '/parcels')
api.add_resource(GetOneParcel, '/parcels/<order_no>')
api.add_resource(CancelParcel, '/parcels/<uuid:order_no>/cancel')
api.add_resource(FetchParcelsByUsers, '/users/<user_id>/parcels')
