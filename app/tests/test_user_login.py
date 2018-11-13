from . import BaseClass


class UserTestCase(BaseClass):
    """This class represents the user test case"""
    def test_user_login_successful(self):
        """Test API user can login(POST request"""
        data ={"email":"langatchirchir@gmail.com",
               "password": "kevin12345",
               "page": "user"}
        res = self.client().post("api/v1/signup", json=self.user)
        res = self.client().post("api/v1/login", json=data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("redirect to user", str(res.data))

    def test_admin_login_success(self):
        """Test API admin can login(POST request)"""
        data = {"email": "admin@gmail.com",
                "password": "admin",
                "page": "admin"}
        res = self.client().post("api/v1/signup", json=self.admin)
        res = self.client().post("api/v1/login", json=data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("redirect to admin", str(res.data))

    def test_user_login_failed(self):
        """Test API user cannot login with wrong login credentials"""
        data = {"email": "langatchirhir@gmail.com",
                "password": "kevin",
                "page": "user"}
        res = self.client().post("api/v1/signup", json=self.user)
        res = self.client().post("api/v1/login", json=data)
        self.assertEqual(res.status_code, 401)
        self.assertIn("email not found", str(res.data))

    def test_user_trying_admin_page(self):
        """Test API if user can access admin page"""
        data = {"email": "langatchirchir@gmail.com",
                "password": "kevin12345",
                "page": "admin"}
        res = self.client().post("api/v1/signup", json=self.user)
        res = self.client().post("api/v1/login", json=data)
        self.assertEqual(res.status_code, 403)
        self.assertIn("you are not an admin", str(res.data))
