"""This is the view for sendit application"""
from flask import Flask, jsonify, make_response
from flask_restplus import Api, Resource
from .models import UserModel
from .models import ParcelModel


app = Flask(__name__)
api = Api(app)


class Users(Resource):
    """This is the user class for signup"""
    def post(self):
        """The post request for the class"""
        payload = api.payload
        # check if payload is empty
        if not payload:
            return {'status': 'failed', 'message': 'provide all fields'}, 400
        if not (payload['email'] or payload['name'] or payload['password'] or payload['role']):
            return {'status': 'failed', 'message': 'bad request refer to API document'}, 400
        user = UserModel()
        data = user.add_user(payload)
        return {'status': 'added', 'message': 'Successfully signed up', 'data': data}, 201


class Login(Resource):
    """The login class that will handle login"""
    def post(self):
        """The post request for login"""
        payload = api.payload
        # Get the variables you'll use
        email = payload['email']
        page = payload['page']
        password_given = payload['password']
        user = UserModel()
        data = user.get_user(email)

        if not data: # returned from our model get_user
            return {'status': 'failed', 'message': 'email not found'}, 401
        role = data['role']
        password = data['password']
        if not password == password_given:
            return {'status': 'failed', 'message': 'wrong password'}, 401
        if page == 'admin' and role == 'user':
            return {'status': 'failed', 'message': 'you are not an admin'}, 403
        return {'status': 'success', 'message': 'redirect to ' + page}, 200


class Parcels(Resource):
    """The parcel class which handles parcels"""
    def post(self):
        """The post request from customer"""
        if not api.payload:
            return {'status': 'failed', 'message': 'please provide a json data'}, 400
        payload = api.payload
        if 'user_id' not in payload:
            return {'status': 'failed', 'message': 'please provide user_id'}, 400
        if 'parcel_type' not in payload:
            return {'status': 'failed', 'message': 'please provide parcel_type'}, 400
        if 'Dest' not in payload:
            return {'status': 'failed', 'message': 'please provide destination'}, 400
        if 'recepient_number' not in payload:
            return {'status': 'failed', 'message': 'please provide receipt_number'}, 400
        parcel = ParcelModel()
        data = parcel.add_parcel(payload)
        return {'status': 'added', 'message': 'Successfully added', 'parcel': data}, 201

    def get(self):
        """This gets all the parcels from the ParcelModel"""
        parcel = ParcelModel()
        parcels = parcel.get_all_parcels()
        if not parcels:
            return {'status': 'success', 'message': 'no parcel submited yet'}, 200
        return {'status': 'success', 'data': parcels}, 200


class GetOneParcel(Resource):
    """This class gets specific parcel"""
    def get(self, order_no):
        """the get request"""
        parcels = ParcelModel()
        parcel = parcels.get_parcel(order_no)
        if not parcel:
            data = {'status': 'failed', 'message': 'not found'}
            return make_response(jsonify(data), 404)
        data = {'status': 'success', 'parcel': parcel}
        return make_response(jsonify(data), 200)


class CancelParcel(Resource):
    """This class cancels the orders"""
    def put(self, order_no):
        """the put request"""
        parcel = ParcelModel()
        cancel = parcel.cancel_parcel(order_no)
        if not cancel:
            return {'status': 'failed', 'message': 'order number not found'}, 404
        if cancel['status'] == 'delivered':
            return {'status': 'failed', 'message': 'Already delivered', "data": cancel}, 403
        if cancel['status'] == 'cancelled':
            return {'status': 'success', 'message': 'processing', "data": cancel}, 202


class FetchAllParcel(Resource):
    """This class gets parcels for a specific user"""
    def get(self, user_id):
        parcel = ParcelModel()
        users = parcel.get_user_parcels(user_id)
        number_of_parcels = str(users['parcels'])  # change from interger to string  to add on the message
        parcels = users['data']
        if not parcels:
            return {'status': 'success', 'message': number_of_parcels + ' parcels found', "data": 'null'}, 404
        return {'status': 'success', 'message': number_of_parcels + ' parcels found', "data": parcels}, 202
