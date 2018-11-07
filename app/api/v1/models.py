from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app)


class Signup(Resource):
    def get(self):
        return {'hey': 'there'}
