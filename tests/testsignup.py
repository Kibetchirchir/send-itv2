import unittest
import os
import json
from app import create_app


class UserTestCase(unittest.TestCase):
    """This class represents the  test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {"name": "chirchir Kibet",
                     "email": "langatchirchir@gmail.com",
                     "role": "user",
                     "password": "kevin12345"
                     }
        self.admin = {"name": "admin",
                      "email": "admin@gmail.com",
                      "role": "admin",
                      "password": "admin"
                     }

    def test_signup(self):
        """Test API can signup (POST request)"""
        res = self.client().post("api/v1/signup", json=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn("chirchir Kibet", str(res.data))

    def test_signup_fail(self):
        """Test API cannot take null (POST request)"""
        res = self.client().post("api/v1/signup", data=self.user)
        self.assertEqual(res.status_code, 400)
        self.assertIn("provide all fields", str(res.data))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()  # Make the tests conveniently executable
