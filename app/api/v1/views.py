"""This is the view for sendit application"""
from flask import Flask, jsonify, make_response
from flask_restplus import Api, Resource
from .models import UserModel
from .models import ParcelModel
from .models import CheckRequired

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    """This is the user class for signup"""
    def post(self):
        """The post request for the class"""
        payload = api.payload
        # check if payload is empty
        check = CheckRequired(payload)
        checked_payload = check.check_payload_signup()
        if not checked_payload:
            return {'status': 'failed', 'message': 'bad request refer to API document or provide all fields'}, 400
        verifier = CheckRequired(payload)
        email_checked = verifier.check_for_email()
        if not email_checked:
            return {'status': 'failed', 'message': 'bad request check your email'}, 400
        email = payload['email']
        user = UserModel()
        data = user.get_user(email)
        if data:
            return {'status': 'failed', 'message': 'conflict email already used'}, 409
        user = UserModel()
        data = user.add_user(payload)
        return {'status': 'added', 'message': 'Successfully signed up', 'data': data}, 201


class Login(Resource):
    """The login class that will handle login"""
    def post(self):
        """The post request for login"""
        payload = api.payload
        # Get the variables you'll use
        if not payload:
            return {'status': 'failed', 'message': 'provide all fields'}, 400
        if not all(key in payload for key in ['email', 'password', 'role']):
            return {'status': 'failed', 'message': 'bad request please provide all fields'}, 400
        email = payload['email']
        role_provided = payload['role']
        password_given = payload['password']
        user = UserModel()
        data = user.get_user(email)
        if not data:  # returned from our model get_user
            return {'status': 'failed', 'message': 'email not found'}, 401
        role = data['role']
        password = data['password']
        if not password == password_given:
            return {'status': 'failed', 'message': 'wrong password'}, 401
        if role_provided == 'admin' and role == 'user':
            return {'status': 'failed', 'message': 'you are not an admin'}, 403
        payload = {"name": data['name'],
                   "role": role,
                   "user_id": data['id']
                   }
        return {'status': 'success', 'message': 'Successful logged in', 'data': payload}, 200


class Parcels(Resource):
    """The parcel class which handles parcels"""
    def post(self):
        """The post request from customer"""
        if not api.payload:
            return {'status': 'failed', 'message': 'please provide a json data'}, 400
        payload = api.payload
        if not all(key in payload for key in ['user_id', 'parcel_type', 'Dest', 'status']):
            return {'status': 'failed', 'message': 'bad request all required fields'}, 400
        check_empty = CheckRequired(payload)
        checked_empty = check_empty.check_data_payload()
        if not checked_empty:
            return {'status': 'failed', 'message': 'bad request no empty value allowed'}, 400
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
        if cancel['status'] == 'pending':
            return {'status': 'success', 'message': 'processing', "data": cancel}, 202


class FetchParcelsByUsers(Resource):
    """This class gets parcels for a specific user"""
    def get(self, user_id):
        parcel = ParcelModel()
        users = parcel.get_user_parcels(user_id)
        number_of_parcels = str(users['parcels'])  # change from interger to string  to add on the message
        parcels = users['data']
        if not parcels:
            return {'status': 'success', 'message': number_of_parcels + ' parcels found', "data": 'null'}, 404
        return {'status': 'success', 'message': number_of_parcels + ' parcels found', "data": parcels}, 202
