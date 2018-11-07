from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)


class SignUp(Resource):
    def get(self):
        pass
    def post(self):
        return {'result': 'added'}, 201

