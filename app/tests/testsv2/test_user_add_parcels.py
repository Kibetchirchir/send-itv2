from . import BaseClass
import json
import pdb


class ParcelTestCase(BaseClass):
    """This test case tets the parcel test cases"""
    def test_user_add_parcel(self):
        """Test API if it adds a parcel(POST)"""
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 201)
        self.assertIn("Successfully added", str(res.data))

    def test_user_add_parcel_bad_Request(self):
        """Test API for bad request"""
        parcel = {"user_id": 1,
                  "parcel_type": "letter",
                  "recepient_number": "254715428709",
                  "status": "on_transit"}
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=parcel, headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 400)
        self.assertIn("bad request", str(res.data))

    def test_empty_fields(self):
        """Docstring testing for  parcel"""
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 400)
        self.assertIn("please provide a json data", str(res.data))

    def test_admin_add_parcel(self):
        data = {"email": "admin@gmail.com",
                "password": "admin",
                "role": "admin"}
        res = self.client().post("api/v2/auth/signup", json=self.admin)
        res = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 403)
        self.assertIn("unauthorized only the user can add a parcel", str(res.data))

    def test_empty_field(self):
        parcel = {"user_id": "d8bae0c0-e974-11e8-a266-b808cf9f9e6c",
                  "parcel_type": "letter",
                  "recepient_number": "428709",
                  "recepient_name": "chirchir",
                  "Dest": "dgfgf",
                  "status": "",
                  "weight": "5",
                  "Dest_from": "df"}
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=parcel, headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 400)
        self.assertIn("bad request no empty value allowed", str(res.data))
