from flask import Flask
from flask_restplus import Api, Resource, fields
from .models import Model

app = Flask(__name__)
api = Api(app)

signup_details = api.model('user', {'user': fields.String('The user name')})


class Users(Resource, Model):
    def get(self):
        pass

    def post(self):
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
