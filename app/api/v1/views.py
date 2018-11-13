from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
from .models import UserModel
from .models import ParcelModel


app = Flask(__name__)
api = Api(app)

signup_details = api.model('user', {'user': fields.String('The user name')})


class Users(Resource, UserModel):
    """This is the user class for signup"""
    def get(self):
        """The get request for the class"""
        pass

    def post(self):
        """The post request for the class"""
        payload = api.payload
        # check if payload is empty
        if not payload:
            return {'result': 'failed', 'message': 'provide all fields'}, 400
        if payload:
            if not (payload['email'] or payload['name'] or payload['password'] or payload['role']):
                return {'result': 'failed', 'message': 'bad request refer to API document'}, 400
            if "email" not in payload:
                return {'result': 'failed', 'message': 'please provide the email'}, 400
            if "name" not in payload:
                return {'result': 'failed', 'message': 'please provide the name'}, 400
            if "password" not in payload:
                return {'result': 'failed', 'message': 'please provide the password'}, 400
            if "role" not in payload:
                return {'result': 'failed', 'message': 'please provide the role'}, 400
            if not payload['email'] and payload['name'] and payload['password'] and payload['role']:
                return {'result': 'failed', 'message': 'bad request refer to API document'}, 400
            if payload['email'] and payload['name'] and payload['password'] and payload['role']:
                user = UserModel()
                data = user.add_user(payload)
                return {'result': 'added', 'message': 'Successfully signed up', 'data': data}, 201


class Login(Resource, UserModel):
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
            return {'result': 'failed', 'message': 'email not found'}, 401
        role = data['role']
        password = data['password']
        if not password == password_given:
            return {'result': 'failed', 'message': 'wrong password'}, 401
        if not (page == "user" or page == "admin"):
            return {'status': 'failed', 'message': 'please provide right information'},400
        if page == "user" and role == 'user':  # checking the page requested
            return {'result': 'success', 'message': 'redirect to user'}, 200
        elif page == "user" and role == 'admin':
            return {'result': 'success', 'message': 'redirect to user'}, 200
        elif page == "admin" and role == 'admin':
            return {'result': 'success', 'message': 'redirect to admin'}, 200
        elif page == "admin" and role == 'user':
            return {'result': 'failed', 'message': 'you are not an admin'}, 403


class Parcels(Resource, ParcelModel):
    """The parcel class which handles parcels"""
    def post(self):
        """The post request from customer"""
        if not api.payload:
            return {'result': 'failed', 'message': 'please provide a json data'}, 400
        if api.payload:
            payload = api.payload
            if not payload['user_id'] or payload['parcel_type'] or payload['Dest'] or payload['recepient_number']:
                return {'result': 'failed', 'message': 'please provide a valid json data refer API doc'}, 400
            if payload['user_id'] or payload['parcel_type'] or payload['Dest'] or payload['recepient_number']:
                if  'user_id' in payload:
                    pass
                else:
                    return {'result': 'failed', 'message': 'please provide user_id'}, 400
                if 'parcel_type' in payload:
                    pass
                else:
                    return {'result': 'failed', 'message': 'please provide parcel_type'}, 400
                if 'Dest' in payload:
                    pass
                else:
                    return {'result': 'failed', 'message': 'please provide destination'}, 400
                if 'recepient_number' in payload:
                    pass
                else:
                    return {'result': 'failed', 'message': 'please provide the recepient number'}, 400
                if payload['user_id'] or payload['parcel_type'] or payload['Dest'] or payload['recepient_number']:
                    parcel = ParcelModel()
                    data = parcel.add_parcel(payload)
                    return {'result': 'added', 'message': 'Successfully added', 'parcel': data}, 201
                else:
                    return {'result': 'failed', 'message': 'please read the api document'}, 400

    def get(self):
        parcel = ParcelModel()
        parcels = parcel.get_all_parcels()
        return {'result': 'success', 'parcels': parcels}, 200


class GetOneParcel(Resource, ParcelModel):
    """This class gets specific parcel"""
    def get(self, order_no):
        """the get request"""
        parcels = ParcelModel()
        parcel = parcels.get_parcel(order_no)
        if parcel == 0:
            return {'result': 'failed', 'message': 'not found'}, 404
        else:
            return {'result': 'success', 'parcel': parcel}, 200


class CancelParcel(Resource, ParcelModel):
    """This class cancels the orders"""
    def put(self, order_no):
        """the put request"""
        parcel = ParcelModel()
        cancel = parcel.cancel_parcel(order_no)
        if cancel == 'cancel': # code for the updated
            return {'result': 'success', 'message': 'processing'}, 202
        elif cancel == 'delivered':  # code for a delivered parcel
            return {'result': 'failed', 'message': 'Already delivered'}, 403
        else:
            return {'result': 'failed', 'message': 'order number not found'}, 404


class FetchAllParcel(Resource, ParcelModel):
    def get(self, user_id):
        parcel = ParcelModel()
        users = parcel.get_user_parcels(user_id)
        return users


