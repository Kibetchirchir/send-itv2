import base64
db = [
    {
        "user": [],
        "parcel": [],
        "tokens": []
    }
    ]


class Model():
    def __init__(self):
        self.db = list(db)

    def add_user(self, data):
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
