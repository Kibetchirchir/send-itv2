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
        self.user = {'name': 'chirchir Kibet',
                     'email': 'langatchirchir@gmail.com',
                     'role': 'user',
                     'password': 'kevin12345'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_signup(self):
        """Test API can signup (POST request)"""
        res = self.client().post('/signup/', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('chirchir Kibet', str(res.data))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()