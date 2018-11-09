import unittest
import os
import json


from app import create_app


class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

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

    def test_user_login_successful(self):
        """Test API user can login(POST request"""
        data ={"email":"langatchirchir@gmail.com",
               "password": "kevin12345",
               "page": "user"}
        res = self.client().post("api/v1/signup", json=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().post("api/v1/login", json=data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("redirect to user", str(res.data))

    def test_admin_login_success(self):
        """Test API admin can login(POST request)"""
        data = {"email": "admin@gmail.com",
                "password": "admin",
                "page": "admin"}
        res = self.client().post("api/v1/signup", json=self.admin)
        self.assertEqual(res.status_code, 201)
        res = self.client().post("api/v1/login", json=data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("redirect to admin", str(res.data))

    def test_user_login_failed(self):
        """Test API user cannot login with wrong login credentials"""
        data = {"email": "langatchirhir@gmail.com",
                "password": "kevin",
                "page": "user"}
        res = self.client().post("api/v1/signup", json=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().post("api/v1/login", json=data)
        self.assertEqual(res.status_code, 401)
        self.assertIn("email not found", str(res.data))

    def test_user_trying_admin_page(self):
        """Test API if user can access admin page"""
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "page": "admin"}
        res = self.client().post("api/v1/signup", json=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().post("api/v1/login", json=data)
        self.assertEqual(res.status_code, 403)
        self.assertIn("you are not an admin", str(res.data))


class ParcelTestCase(unittest.TestCase):
    """This test case tets the parcel test cases"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.parcel = {"user_id": 1,
                       "parcel_type": "letter",
                       "recepient_number": "254715428709",
                       "Dest": "Moi_avenue",
                       "status": "on_transit"
                       }

    def test_user_add_parcel(self):
        """Test API if it adds a parcel(POST)"""
        res = self.client().post("api/v1/parcels", json=self.parcel)
        self.assertEqual(res.status_code, 201)
        self.assertIn("order_no", str(res.data))

    def test_user_add_parcel_bad_Request(self):
        """Test API for bad request"""
        parcel = {"user_id": 1,
                  "parcel_type": "letter",
                  "recepient_number": "254715428709",
                  "status": "on_transit"
                  }
        res = self.client().post("api/v1/parcels", json=parcel)
        self.assertEqual(res.status_code, 400)
        self.assertIn("destination", str(res.data))

    def test_admin_all_parcels(self):
        """Test API for getting all parcels (GET_REQUEST)"""
        res = self.client().post("api/v1/parcels", json=self.parcel)
        self.assertEqual(res.status_code, 201)
        res = self.client().get("api/v1/parcels")
        self.assertEqual(res.status_code, 200)
        self.assertIn("254715428709", str(res.data))

    def test_specific_parcels(self):
        """Test API for getting a specific parcel using the order number"""
        res = self.client().post("api/v1/parcels", json=self.parcel)
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data(as_text=True))
        order_no = data['parcel']['order_no']
        order_no = str(order_no)
        res = self.client().get("api/v1/parcels/"+order_no)
        self.assertEqual(res.status_code, 200)
        self.assertIn("254715428709", str(res.data))

    def test_specific_parcel_fail(self):
        """Test API for getting a specific parcel with wrong order_number"""
        res = self.client().get("api/v1/parcels/fnfnf")
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found", str(res.data))

    def test_user_can_cancel(self):
        """Test API for cancelling parcel(PUT method)"""
        res = self.client().post("api/v1/parcels", json=self.parcel)
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data(as_text=True))
        order_no = data['parcel']['order_no']
        order_no = str(order_no)
        res = self.client().put("api/v1/parcels/" + order_no + "/cancel")
        self.assertEqual(res.status_code, 202)
        self.assertIn("processing", str(res.data))

    def test_user_cannot_cancel_delivered(self):
        """Test API for cancelling delivered parcel(PUT method)"""
        parcel = {"user_id": 1,
                  "parcel_type": "letter",
                  "recepient_number": "254715428709",
                  "Dest": "Moi_avenue",
                  "status": "delivered"
                  }
        res = self.client().post("api/v1/parcels", json=parcel)
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data(as_text=True))
        order_no = data['parcel']['order_no']
        order_no = str(order_no)
        res = self.client().put("api/v1/parcels/" + order_no + "/cancel")
        self.assertEqual(res.status_code, 403)
        self.assertIn("failed", str(res.data))

    def test_get_all_parcels_for_user(self):
        """Test API for getting a all parcels created by a user"""
        parcel = {"user_id": 4,
                  "parcel_type": "letter",
                  "recepient_number": "254715428709",
                  "Dest": "Moi_avenue",
                  "status": "delivered"
                  }
        res = self.client().post("api/v1/parcels", json=parcel)
        self.assertEqual(res.status_code, 201)
        res = self.client().get("api/v1/users/4/parcels")
        self.assertEqual(res.status_code, 200)
        self.assertIn("254715428709", str(res.data))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
