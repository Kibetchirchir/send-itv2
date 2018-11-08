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
        # check if payload is empty
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
        # Get the variables you'll use
        email = payload['email']
        page = payload['page']
        password_given = payload['password']
        user = Model()
        data = user.get_user(email)
        status = data['status'] # 1 rep email is found 0 rep email was not found

        if status == 1:
            # get the data from model
            role = data['role']
            password = data['password']
            if password == password_given:
                if page == "user" and role == 'user':  # checking the page requested
                    return {'result': 'success', 'message': 'redirect to user'}, 303
                elif page == "user" and role == 'admin':
                    return {'result': 'success', 'message': 'redirect to user'}, 303
                elif page == "admin" and role == 'admin':
                    return {'result': 'success', 'message': 'redirect to admin'}, 303
                elif page == "admin" and role == 'user':
                    return {'result': 'failed', 'message': 'you are not an admin'}, 403
            else:
                return {'result': 'failed', 'message': 'wrong password'}, 401
        else:
            return {'result': 'failed', 'message': 'email not found'}, 401
