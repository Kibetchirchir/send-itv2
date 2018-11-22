import unittest


from app import create_app
from ...db_config import destroy_tables


class BaseClass(unittest.TestCase):
    """This base class for our testcases"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user = {"name": "chirchir Kibet",
                     "email": "langatchirchir@gmail.com",
                     "role": "user",
                     "password": "kevin12345"}
        self.admin = {"name": "admin",
                      "email": "admin@gmail.com",
                      "role": "admin",
                      "password": "admin"}
        self.parcel = {"user_id": "d8bae0c0-e974-11e8-a266-b808cf9f9e6c",
                       "parcel_type": "letter",
                       "recepient_number": "428709",
                       "recepient_name": "chirchir",
                       "Dest": "dgfgf",
                       "status": "delivered",
                       "weight": "5",
                       "Dest_from": "df"}

    def tearDown(self):
        destroy_tables()
