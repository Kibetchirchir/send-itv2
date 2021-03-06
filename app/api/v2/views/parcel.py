""""This is the view for sendit application"""
from flask import Flask, jsonify, make_response
from flask_restplus import Api, Resource
from ..models.parcel import ParcelModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from .validator import CheckRequired
from .mailing import SendMail
from .user import UserModel

app = Flask(__name__)
api = Api(app)


class Parcels(Resource):
    """The parcel class which handles parcels"""
    @jwt_required
    def post(self):
        """The post request from customer"""
        if not api.payload:
            return {'status': 'failed', 'message': 'please provide a json data'}, 400
        payload = api.payload
        if not all(key in payload for key in ['parcel_type', 'drop_off_location', 'pick_up_location',
                                              'status']):
            return {'status': 'failed', 'message': 'bad request all required fields'}, 400
        check_empty = CheckRequired(payload)
        checked_empty = check_empty.check_data_payload()
        current_user = get_jwt_identity()
        role = current_user['role']
        if role == 'admin':
            return {'status': 'failed', 'message': 'Only authorized users can add a parcel'}, 403
        if not checked_empty:
            return {'status': 'failed', 'message': 'bad request no empty value allowed'}, 400
        parcel = ParcelModel()
        user_id = current_user['user_id']
        data = parcel.add_parcel(payload, user_id)
        return {'status': 'added', 'message': 'Successfully added', 'parcel': data}, 201

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        role = current_user['role']
        user_id = current_user['user_id']
        parcel = ParcelModel()
        parcels = parcel.get_all_parcels(role, user_id)
        if not parcels:
            return {'status': 'success', 'message': "no parcels posted yet"}, 200
        return {'status': 'success', 'message': parcels}, 200


class ParcelChangeDestination(Resource):
    @jwt_required
    def put(self, parcelid):
        """This is the end point for changing the parcel destination"""
        payload = api.payload
        if not payload:
            return {'status': 'failed', 'message': 'please provide a json data'}, 400
        if not all(key in payload for key in ['dest']):
            return {'status': 'failed', 'message': 'please provide the destination'}, 400
        check_empty = CheckRequired(payload)
        checked_empty = check_empty.check_data_payload()
        if not checked_empty:
            return {'status': 'failed', 'message': 'bad request no empty value allowed'}, 400
        parcel = ParcelModel()
        parcels = parcel.get_parcel(parcelid)
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        if not parcels:
            return {'status': 'failed', 'message': 'parcel ID does not exist', "data": parcels}, 404
        if not user_id == parcels['user_id']:
            return {'status': 'failed', 'message': 'you are not allowed to change the following '
                                                   'parcel destination'}, 403
        if parcels['status'] == 'delivered':
            return {'status': 'failed', 'message': 'Already delivered', "data": parcels}, 403
        change = parcel.change_dest(payload['dest'], parcelid)
        if not change:
            return {'status': 'failed', 'message': 'There was an error processing data'}, 500
        parcels['status'] = "processing"
        return {'status': 'success', 'message': 'processing', "data": parcels}, 202


class AdminChangeStatus(Resource):
    """Admin can change the status of the parcel"""
    @jwt_required
    def put(self, parcelid):
        payload = api.payload
        if not payload:
            return {'status': 'failed', 'message': 'please provide a json data'}, 400
        if not all(key in payload for key in ['status']):
            return {'status': 'failed', 'message': 'please provide the destination'}, 400
        check_empty = CheckRequired(payload)
        checked_empty = check_empty.check_data_payload()
        if not checked_empty:
            return {'status': 'failed', 'message': 'bad request no empty value allowed'}, 400
        parcel = ParcelModel()
        parcels = parcel.get_parcel(parcelid)
        current_user = get_jwt_identity()
        role = current_user['role']
        if not role == 'admin':
            return {'status': 'failed', 'message': 'Unauthorised. you are not allowed'}, 403
        if not parcels:
            return {'status': 'failed', 'message': 'parcel ID does not exist', "data": parcels}, 404
        change = parcel.change_status(payload['status'], parcelid)
        if not change:
            return {'status': 'failed', 'message': 'There was an error processing data'}, 500
        parcels['status'] = "processing"
        return {'status': 'success', 'message': 'Waiting for confirmation', "data": parcels}, 202


class AdminChangeLocation(Resource):
    """Admin can change the destination of the parcel"""
    @jwt_required
    def put(self, parcelid):
        payload = api.payload
        if not payload:
            return {'status': 'failed', 'message': 'please provide a json data'}, 400
        if not all(key in payload for key in ['location']):
            return {'status': 'failed', 'message': 'please provide the destination'}, 400
        check_empty = CheckRequired(payload)
        checked_empty = check_empty.check_data_payload()
        if not checked_empty:
            return {'status': 'failed', 'message': 'bad request no empty value allowed'}, 400
        parcel = ParcelModel()
        parcels = parcel.get_parcel(parcelid)
        current_user = get_jwt_identity()
        role = current_user['role']
        if not role == 'admin':
            return {'status': 'failed', 'message': 'Unauthorised. you are not allowed'}, 403
        if not parcels:
            return {'status': 'failed', 'message': 'parcel ID does not exist', "data": parcels}, 404
        change = parcel.change_location(payload['location'], parcelid)
        if not change:
            return {'status': 'failed', 'message': 'There was an error processing data'}, 500
        parcels['current_location'] = payload['location']
        # get the user_id
        user_id = parcels["user_id"]
        # Get the user email
        user = UserModel()
        user_data = user.get_user_email(user_id)
        user_email = user_data[1]
        message = "Hey Customer the current location of your parcel " + parcelid + " is now in\n" \
                                                                                   "" + parcels['current_location']
        email = SendMail()
        email.send_mail(message, user_email, "Parcel update")
        return {'status': 'success', 'message': 'Waiting for confirmation', "data": parcels}, 202
