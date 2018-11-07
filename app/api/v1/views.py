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

        user = Model()
        data = user.add_user(api.payload)
        return {'result': 'added', 'message':'Successfully signed up', 'data': data}, 201
