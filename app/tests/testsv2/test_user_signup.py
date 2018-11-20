from . import BaseClass


class UserTestCase(BaseClass):
    """This class represents the user test case"""
    def test_signup(self):
        """Test API can signup (POST request)"""
        user = {"name": "chirchir Kibet",
                "email": "chirchir@gmail.com",
                "role": "user",
                "password": "kevin12345"}
        res = self.client().post("api/v2/auth/signup", json=user)
        self.assertEqual(res.status_code, 201)
        self.assertIn("chirchir Kibet", str(res.data))

    def test_signup_fail(self):
        """Test API cannot take null (POST request)"""
        res = self.client().post("api/v2/auth/signup", data=self.user)
        self.assertEqual(res.status_code, 400)
        self.assertIn("provide all fields", str(res.data))

    def test_email_repeat(self):
        res = self.client().post("api/v2/auth/signup", json=self.user)
        self.assertEqual(res.status_code, 409)
        self.assertIn("conflict email already used", str(res.data))

    def test_validate_email(self):
        """Test API cannot take unvalidated email (POST request)"""
        user = {"name": "chirchir Kibet",
                "email": "chirchirgmail.com",
                "role": "user",
                "password": "kevin12345"}
        res = self.client().post("api/v2/auth/signup", json=user)
        self.assertEqual(res.status_code, 400)
        self.assertIn("check your email", str(res.data))
