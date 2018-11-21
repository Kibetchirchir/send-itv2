"""Docstring for our validator"""


class CheckRequired:
    """This class check the required fields are filled"""
    def __init__(self, payload):
        self.payload = payload

    def check_payload_signup(self):
        """To check if payload is not empty and all values are provided"""
        if not self.payload:
            return False
        if all(key in self.payload for key in ['email', 'password', 'role', 'name']):
                values = CheckRequired(self.payload)
                values_return = values.check_data_payload()
                if values_return:
                    return self.payload

    def check_data_payload(self):
        """To check all are not empty"""
        if not any(value == "" for value in self.payload.values()):
            return self.payload

    def check_for_email(self):
        """To check for email"""
        email = self.payload['email']
        if any(value == "@" for value in email):
            if any(value == "." for value in email):
                return self.payload
