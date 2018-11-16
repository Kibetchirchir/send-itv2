from . import BaseClass


class UserTestCase(BaseClass):
    """This class represents the RESOURCE NOT FOUND test"""
    def test_for_wrong_url(self):
        """Test API returns messsage when given wrong URL"""
        res = self.client().get("api/v1/users/4/parcelss")
        self.assertEqual(res.status_code, 404)
        self.assertIn("Check your url", str(res.data))
