"""This is the view for sendit application"""
from flask import Flask
from flask_restplus import Api, Resource
from ..models.user import UserModel
from .validator import CheckRequired
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

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
            return {'status': 'failed', 'message': 'bad request Invalid email'}, 400
        email = payload['email']
        user = UserModel()
        data = user.get_user(email)
        if data:
            return {'status': 'failed', 'message': 'Conflicting data. Email already exists'}, 409
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
        # returned from our model get_user
        if not data:
            return {'status': 'failed', 'message': 'email not found'}, 401
        # True for admin and False for user
        role = data[4]
        if role:
            role = "admin"
        else:
            role = "user"
        password = data[2]
        name = data[3]
        if not check_password_hash(password, password_given):
            return {'status': 'failed', 'message': 'wrong password'}, 401
        if role_provided == 'admin' and role == 'user':
            return {'status': 'failed', 'message': 'you are not an admin'}, 403
        payload = {"name": name,
                   "role": role,
                   "user_id": data[0],
                   }
        access_token = create_access_token(identity=payload)
        payload['token'] = access_token
        return {'status': 'success', 'message': 'Successful logged in', 'data': payload}, 200
