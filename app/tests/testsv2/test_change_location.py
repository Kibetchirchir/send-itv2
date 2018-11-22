import json
from . import BaseClass


class ParcelTestCase(BaseClass):
    """This test case tets the parcel test cases"""
    def test_admin_change_location(self):
        """Test API if it adds a parcel(POST)"""
        data = {"email": "admin@gmail.com",
                "password": "admin",
                "role": "admin"}
        data2 = {"email": "langatchirchir@gmail.com",
                 "password": "kevin12345",
                 "role": "user"}
        location = {"location": "Nairobi"}
        res = self.client().post("api/v2/auth/signup", json=self.admin)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token_admin = data['data']['token']
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data2)
        data = json.loads(res2.get_data(as_text=True))
        token_user = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token_user))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        res = self.client().put("api/v2/parcels/" + order_id + "/presentLocation", json=location,
                                headers=dict(Authorization="Bearer " + token_admin))
        self.assertEqual(res.status_code, 202)
        self.assertIn("Nairobi", str(res.data))

    def test_empty_payload(self):
        """This test if our api can process an empty payload"""
        data = {"email": "admin@gmail.com",
                "password": "admin",
                "role": "admin"}
        data2 = {"email": "langatchirchir@gmail.com",
                 "password": "kevin12345",
                 "role": "user"}
        res = self.client().post("api/v2/auth/signup", json=self.admin)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token_admin = data['data']['token']
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data2)
        data = json.loads(res2.get_data(as_text=True))
        token_user = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token_user))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        res = self.client().put("api/v2/parcels/" + order_id + "/presentLocation",
                                headers=dict(Authorization="Bearer " + token_admin))
        self.assertEqual(res.status_code, 400)
        self.assertIn("please provide a json data", str(res.data))

    def test_location_not_provided(self):
        data = {"email": "admin@gmail.com",
                "password": "admin",
                "role": "admin"}
        data2 = {"email": "langatchirchir@gmail.com",
                 "password": "kevin12345",
                 "role": "user"}
        not_location = {"not_status": "delivered"}
        res = self.client().post("api/v2/auth/signup", json=self.admin)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token_admin = data['data']['token']
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data2)
        data = json.loads(res2.get_data(as_text=True))
        token_user = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token_user))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        res = self.client().put("api/v2/parcels/" + order_id + "/presentLocation", json=not_location,
                                headers=dict(Authorization="Bearer " + token_admin))
        self.assertEqual(res.status_code, 400)
        self.assertIn("please provide the destination", str(res.data))

    def test_empty_dest(self):
        data = {"email": "admin@gmail.com",
                "password": "admin",
                "role": "admin"}
        location = {"location": ""}
        res = self.client().post("api/v2/auth/signup", json=self.admin)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().put("api/v2/parcels/hghghghg/presentLocation", json=location,
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 400)
        self.assertIn("bad request no empty value allowed", str(res.data))

    def test_unexisting_parcel(self):
        data = {"email": "admin@gmail.com",
                "password": "admin",
                "role": "admin"}
        location = {"location": "Nairobi"}
        res = self.client().post("api/v2/auth/signup", json=self.admin)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        order_id = "kdfjbhdfbhsdbhfbcdshfb"
        res = self.client().put("api/v2/parcels/" + order_id + "/presentLocation", json=location,
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 404)
        self.assertIn("parcel ID does not exist", str(res.data))

    def test_user_change(self):
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        location = {"location": "Nairobi"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        res = self.client().put("api/v2/parcels/" + order_id + "/presentLocation", json=location,
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 403)
        self.assertIn("you are not allowed", str(res.data))
