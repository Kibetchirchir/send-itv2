"""This is the view for sendit application"""
from flask import Flask, jsonify, make_response
from flask_restplus import Api, Resource
from ..models.user import UserModel
from .validator import CheckRequired

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
