import base64
import random

db = [
    {
        "user": [],
        "parcel": [],
        "tokens": []
    }
    ]
parcel = []


class Model:
    """This is the model class to manipulate data"""
    def __init__(self):
        """initialzation for our data"""
        self.db = list(db)

    def add_user(self, data):
        """this adds users to our dict"""
        user = self.db[0]['user']
        user_id = len(user) + 1
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
        user = self.db[0]['user']
        array_len = len(user) - 1
        # The array to loop
        i = 0
        while i <= array_len:
            if user[i]['email'] == email:
                name = user[i]['email']
                role = user[i]['role']
                password = user[i]['password']
                payload = {'name' : name,
                           "role": role,
                           "password": password,
                           "status": 1}
                return payload
            else:
                i = i + 1
        payload = {"status": 0}
        return payload

    def add_parcel(self, data):
        """This model adds parcels to our datastructure"""
        parcel = self.db[0]['parcel']
        order_number = random.randint(1000, 9999)
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
        parcels = self.db[0]['parcel']
        return parcels

    def get_parcel(self, order_id):
        parcel = self.db[0]['parcel']
        array_length = len(parcel) - 1
        i = 0  # this is the value to append to my array
        while i <= array_length:
            if parcel[i]['order_no'] == order_id:
                parcel_type = parcel[i]['parcel_type']
                user_id = parcel[i]['user_id']
                dest = parcel[i]['dest']
                recepient_no = parcel[i]['recepient_no']
                parcel = {"parcel_type": parcel_type,
                          "user_id": user_id,
                          "destination": dest,
                          "recepient_no": recepient_no
                          }
                return parcel
            else:
                i = i + 1
        return 0

    def cancel_parcel(self, order_id):
        parcel = self.db[0]['parcel']
        array_length = len(parcel) - 1
        i = 0  # this is the value to append to my array
        while i <= array_length:
            if parcel[i]['order_no'] == order_id:
                parcel_type = parcel[i]['parcel_type']
                user_id = parcel[i]['user_id']
                dest = parcel[i]['dest']
                recepient_no = parcel[i]['recepient_no']
                status = parcel[i]['status']
                if status == 'on_transit':
                    parcel[i]['status'] = 'cancel'
                    return parcel[i]['status']
                else:
                    return parcel[i]['status']
            else:
                i = i + 1
        return 0

    def get_user_parcels(self, user_id):
        parcel = self.db[0]['parcel']
        array_length = len(parcel) - 1
        i = 0  # this is the value to append to my array
        while i <= array_length:
            if parcel[i]["user_id"] == user_id:
                parcel.append(parcel[i])
                i = i + 1
            else:
                i = i + 1
        return parcel

