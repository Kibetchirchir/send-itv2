import unittest


from app import create_app


class BaseClass(unittest.TestCase):
    """This base class for our testcases"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {"name": "chirchir Kibet",
                     "email": "langatchirchir@gmail.com",
                     "role": "user",
                     "password": "kevin12345"}
        self.admin = {"name": "admin",
                      "email": "admin@gmail.com",
                      "role": "admin",
                      "password": "admin"}
        self.parcel = {"user_id": 1,
                       "parcel_type": "letter",
                       "recepient_number": "254715428709",
                       "Dest": "Moi_avenue",
                       "status": "on_transit"}
