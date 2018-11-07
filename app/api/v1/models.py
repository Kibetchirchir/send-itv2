db = [
    {
        "user": [],
        "parcel": []
    }
    ]


class Model():
    def __init__(self):
        self.db = db

    def add_user(self, data):
        user = self.db[0]['user']
        user.append(data)
        return data

    