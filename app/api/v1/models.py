import uuid
import datetime

users = []
parcels = []


class UserModel:
    """This is the model class to manipulate data"""
    def __init__(self):
        """Initialzation for our data"""
        self.users = users

    def add_user(self, data):
        """this adds users to our dict"""
        user = self.users
        user_id = str(uuid.uuid1())
        user_name = data['name']
        user_email = data['email']
        user_password = data['password']
        user_role = data['role']

        payload = {"id": user_id,
                   "name": user_name,
                   "email": user_email,
                   "password": user_password,
                   "role": user_role}

        user.append(payload)
        return payload['name']

    def get_user(self, email):
        """This gets a specific user values"""
        users = self.users
        for user in users:
            if user['email'] == email:
                return user


class ParcelModel:
    """"This is the class parcel model for testing model"""

    def __init__(self):
        """initialzation for our data"""
        self.parcels = parcels

    def add_parcel(self, data):
        """This method adds parcels to our parcels"""
        parcel = self.parcels
        order_number = str(uuid.uuid1())
        parcel_type = data['parcel_type']
        user_id = data['user_id']
        dest = data['Dest']
        status = data['status']
        timestamp = str(datetime.datetime.now())
        recepient = data['recepient_number']
        payload = {"order_no": order_number,
                   "parcel_type": parcel_type,
                   "user_id": user_id,
                   "dest": dest,
                   "recepient_no": recepient,
                   "status": status,
                   "ordered_date": timestamp
                   }
        parcel.append(payload)
        return payload

    def get_all_parcels(self):
        """This method gets all parcels from our parcels"""
        parcels = self.parcels
        return parcels

    def get_parcel(self, order_id):
        """This method gets a specific parcel interms of order_id"""
        parcels = self.parcels
        for parcel in parcels:
            # to change to string for comparison
            parcel_order_no = parcel['order_no']
            # order_id = str(order_id)
            if parcel_order_no == order_id:
                return parcel

    def cancel_parcel(self, order_id):
        """This method cancels a parcel that has not been delivered"""
        parcels = self.parcels
        for parcel in parcels:
            if parcel['order_no'] == str(order_id):
                if parcel['status'] == 'delivered':
                    return parcel
                parcel['status'] = 'pending'
                return parcel

    def get_user_parcels(self, user_id):
        """This method gets all parcels by a specific user"""
        parcels = self.parcels
        # this is for counting how many parcels are there
        count = 0
        user_parcels = []
        for parcel in parcels:
            parcel_user_id = str(parcel['user_id'])
            if parcel_user_id == user_id:
                user_parcels.append(parcel)
                count = count + 1
        return {"data": user_parcels, "parcels": count}


class CheckRequired:
    """This class check the required fields are filled"""
    def __init__(self, payload):
        self.payload = payload

    def check_payload_signup(self):
        """To check if payload is not empty and all values are provided"""
        if not self.payload:
            return False
        if all(key in self.payload for key in ['email', 'password', 'role', 'name']):
                values = CheckRequired(self.payload)
                values_return = values.check_data_payload()
                if values_return:
                    return self.payload

    def check_data_payload(self):
        """To check all are not empty"""
        if not any(value == "" for value in self.payload.values()):
            return self.payload

    def check_for_email(self):
        """To check for email"""
        email = self.payload['email']
        if any(value == "@" for value in email):
            if any(value == "." for value in email):
                return self.payload
