"""DOcstring register our Resource"""
from flask import Blueprint
from flask_restful import Api
from .views.user import Users
from .views.user import Login
from .views.parcel import Parcels, ParcelChangeDestination


v2 = Blueprint('apiv2', __name__, url_prefix=("/api/v2"))
api = Api(v2)

api.add_resource(Users, '/auth/signup', strict_slashes=False)
api.add_resource(Login, '/auth/login', strict_slashes=False)
api.add_resource(Parcels, '/parcels', strict_slashes=False)
api.add_resource(ParcelChangeDestination, '/parcels/<parcelid>/destination', strict_slashes=False)



