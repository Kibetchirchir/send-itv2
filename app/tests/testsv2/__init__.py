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
        self.parcel = {"parcel_type": "box",
                       "recepient_number": "254715428709",
                       "recepient_name": "chirchir",
                       "drop_off_location": "dgfgf",
                       "status": "not-picked",
                       "weight": "5",
                       "pick_up_location": "df"}

    def tearDown(self):
        destroy_tables()
