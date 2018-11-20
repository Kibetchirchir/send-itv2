"""This is the view for sendit application"""
from flask import Flask, jsonify, make_response
from flask_restplus import Api, Resource
from ..models.user import UserModel

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    """This is the user class for signup"""
    def post(self):
        """The post request for the class"""
        payload = api.payload
        if not payload:
            return {'status': 'failed', 'message': 'bad request refer to API document or provide all fields'}, 400
        user = UserModel()
        data = user.add_user(payload)
        return {'status': 'added', 'message': 'Successfully signed up', 'data': data}, 201
