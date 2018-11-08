from flask import Flask
from flask_restplus import Api, Resource, fields
from .models import Model

app = Flask(__name__)
api = Api(app)

signup_details = api.model('user', {'user': fields.String('The user name')})


class Users(Resource, Model):
    """This is the user class for signup"""
    def get(self):
        """The get request for the class"""
        pass

    def post(self):
        """The post request for the class"""
        payload = api.payload
        if payload:

            if payload['email'] or payload['name'] or payload['password'] or payload['role']:
                if "email" in payload:
                    pass
                else:
                    return {'result': 'failed', 'message': 'please provide the email'}, 400
                if "name" in payload:
                    pass
                else:
                    return {'result': 'failed', 'message': 'please provide the name'}, 400
                if "password" in payload:
                    pass
                else:
                    return {'result': 'failed', 'message': 'please provide the password'}, 400
                if "role" in payload:
                    pass
                else:
                    return {'result': 'failed', 'message': 'please provide the role'}, 400
                if payload['email'] and payload['name'] and payload['password'] and payload['role']:
                    user = Model()
                    data = user.add_user(payload)
                    return {'result': 'added', 'message': 'Successfully signed up', 'data': data}, 201
                else:
                    return {'result': 'failed', 'message': 'bad request refer to API document'}, 400

        else:
            return {'result': 'failed', 'message': 'provide all fields'}, 400


class Login(Resource, Model):
    """The login class that will handle login"""
    def post(self):
        """The post request for login"""
        payload = api.payload
        email = payload['email']
        user = Model()
        data = user.get_user(email)
        if data['status'] == 1:
            if payload['page'] == "user" and data['role'] == 'user':  # checking the page requested
                return {'result': 'success', 'message': 'redirect to user', 'data': data}, 303
            elif payload['page'] == "user" and data['role'] == 'admin':
                return {'result': 'success', 'message': 'redirect to user', 'data': data}, 303
            elif payload['page'] == "admin" and data['role'] == 'admin':
                return {'result': 'success', 'message': 'redirect to user', 'data': data}, 303

        else:
            return {'result': 'failed', 'message': 'email not found'}, 401

