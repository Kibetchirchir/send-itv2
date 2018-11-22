import json
from . import BaseClass


class ParcelTestCase(BaseClass):
    """This test case tets the parcel test cases"""
    def test_user_add_parcel(self):
        """Test API if it adds a parcel(POST)"""
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        location = {"dest": "Juja"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        res = self.client().put("api/v2/parcels/" + order_id + "/destination", json=location,
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 202)
        self.assertIn("processing", str(res.data))

    def test_empty_payload(self):
        """This test if our api can process an empty payload"""
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        location = {"dest": "Juja"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        res = self.client().put("api/v2/parcels/" + order_id + "/destination",
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 400)
        self.assertIn("please provide a json data", str(res.data))

    def test_dest_not_provided(self):
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        location = {"location": "Juja"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        res = self.client().put("api/v2/parcels/" + order_id + "/destination", json=location,
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 400)
        self.assertIn("please provide the destination", str(res.data))

    def test_empty_dest(self):
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        location = {"dest": ""}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        res = self.client().put("api/v2/parcels/" + order_id + "/destination", json=location,
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 400)
        self.assertIn("bad request no empty value allowed", str(res.data))

    def test_unexisting_parcel(self):
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        location = {"dest": "juja"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        order_id = "kdfjbhdfbhsdbhfbcdshfb"
        res = self.client().put("api/v2/parcels/" + order_id + "/destination", json=location,
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 404)
        self.assertIn("parcel ID does not exist", str(res.data))

    def test_different_user_change(self):
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        user2 = {"name": "chirchir Kibet",
                 "email": "langat@gmail.com",
                 "role": "user",
                 "password": "kevin123"}
        location = {"dest": "juja"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        # sign up user 2
        res = self.client().post("api/v2/auth/signup", json=user2)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        # login our user 2
        data2 = {"email": "langat@gmail.com",
                 "password": "kevin123",
                 "role": "user"}
        res2 = self.client().post("api/v2/auth/login", json=data2)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().put("api/v2/parcels/" + order_id + "/destination", json=location,
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 403)
        self.assertIn("you are not allowed ", str(res.data))

    def test_user_cannot_change_delivered(self):
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        location = {"dest": "Juja"}
        parcel = {"user_id": "d8bae0c0-e974-11e8-a266-b808cf9f9e6c",
                  "parcel_type": "letter",
                  "recepient_number": "428709",
                  "recepient_name": "chirchir",
                  "drop_off_location": "dgfgf",
                  "status": "delivered",
                  "weight": "5",
                  "pick_up_location": "df"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=parcel, headers=dict(Authorization="Bearer " + token))
        data = json.loads(res.get_data(as_text=True))
        order_id = data['parcel']['order_no']
        res = self.client().put("api/v2/parcels/" + order_id + "/destination", json=location,
                                headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 403)
        self.assertIn("Already delivered", str(res.data))

