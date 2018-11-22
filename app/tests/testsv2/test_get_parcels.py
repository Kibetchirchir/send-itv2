from . import BaseClass
import json


class ParcelTestCase(BaseClass):
    """This test case tets the parcel test cases"""
    def test_user_get_parcel(self):
        """Test API if  user gets a parcel(GET)"""
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        res = self.client().get("api/v2/parcels", headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 200)
        self.assertIn("success", str(res.data))

    def test_no_parcel(self):
        """test for parcel when there are no parcels posed"""
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().get("api/v2/parcels", headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 200)
        self.assertIn("no parcels posted yet", str(res.data))

    def test_admin_get_parcel(self):
        """Test API if  admin can gets all parcel(GET)"""
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "role": "user"}
        res = self.client().post("api/v2/auth/signup", json=self.user)
        res2 = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res2.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().post("api/v2/parcels", json=self.parcel, headers=dict(Authorization="Bearer " + token))
        data = {"email": "admin@gmail.com",
                "password": "admin",
                "role": "admin"}
        res = self.client().post("api/v2/auth/signup", json=self.admin)
        res = self.client().post("api/v2/auth/login", json=data)
        data = json.loads(res.get_data(as_text=True))
        token = data['data']['token']
        res = self.client().get("api/v2/parcels", headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, 200)
        self.assertIn("no parcels posted yet", str(res.data))

