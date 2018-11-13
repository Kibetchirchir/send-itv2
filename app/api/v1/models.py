import random
import uuid

users = []
parcels = []


class UserModel:
    """This is the model class to manipulate data"""
    def __init__(self):
        """initialzation for our data"""
        self.users = users

    def add_user(self, data):
        """this adds users to our dict"""
        user = self.users
        user_id = uuid.uuid4()
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
        order_number = str(uuid.uuid4())
        parcel_type = data['parcel_type']
        user_id = data['user_id']
        dest = data['Dest']
        status = data['status']
        recepient = data['recepient_number']
        payload = {"order_no": order_number,
                   "parcel_type": parcel_type,
                   "user_id": user_id,
                   "dest": dest,
                   "recepient_no": recepient,
                   "status": status
                   }
        parcel.append(payload)
        return payload

    def get_all_parcels(self):
        """This method gets all parcels from our parcels"""
        parcels = self.parcels
        return parcels

    def get_parcel(self, order_id):
        """This method gets a specific parcel interms of order_id"""
        parcel = self.parcels
        for parcel in parcels:
            if parcel['order_no'] == order_id:
                return parcel

    def cancel_parcel(self, order_id):
        """This method cancels a parcel that has not been delivered"""
        parcels = self.parcels
        for parcel in parcels:
            if parcel['order_no'] == order_id:
                if parcel['status'] == 'delivered':
                    return parcel
                parcel['status'] = 'cancelled'
                return parcel

    def get_user_parcels(self, user_id):
        """This method gets all parcels by a specific user"""
        parcels = self.parcels
        count = 0 # this is for counting how many parcels are there
        user_parcels = []
        for parcel in parcels:
            parcel_user_id = str(parcel['user_id'])
            if parcel_user_id == user_id:
                user_parcels.append(parcel)
                count = count + 1
        return {"data": user_parcels, "parcels": count}
