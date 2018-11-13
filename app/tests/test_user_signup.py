from . import BaseClass


class UserTestCase(BaseClass):
    """This class represents the user test case"""
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
