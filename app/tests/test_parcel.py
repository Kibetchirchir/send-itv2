import json
from . import Baseclass


from app import create_app


class ParcelTestCase(Baseclass):
    """This test case tets the parcel test cases"""
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

    def test_get_all_parcels(self):
        """Test API for getting all parcels (GET_REQUEST)"""
        res = self.client().post("api/v1/parcels", json=self.parcel)
        res = self.client().get("api/v1/parcels")
        self.assertEqual(res.status_code, 200)
        self.assertIn("254715428709", str(res.data))

    def test_specific_parcels(self):
        """Test API for getting a specific parcel using the order number"""
        res = self.client().post("api/v1/parcels", json=self.parcel)
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
        res = self.client().get("api/v1/users/4/parcels")
        self.assertEqual(res.status_code, 202)
        self.assertIn("254715428709", str(res.data))
