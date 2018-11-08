import base64
db = [
    {
        "user": [],
        "parcel": [],
        "tokens": []
    }
    ]


class Model():
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
                return (payload)
            else:
                i = i + 1
        payload = {"status": 0}
        return (payload)


