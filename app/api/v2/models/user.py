"""Docstring for models."""
from ....db_config import init_db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel:
    """This is the model class to manipulate user data"""
    def __init__(self):
        """Docstring initialize our connection"""
        self.con = init_db()

    def add_user(self, data):
        """this adds users to our dict"""
        user_name = data['name']
        user_email = data['email']
        user_password = generate_password_hash(data['password'])
        user_role = data['role']
        if user_role == "admin":
            role = 1
        else:
            role = 0
        query = """ INSERT INTO users(email, password, user_name, is_admin, is_active)
                    values
                    ('{}','{}','{}','{}','{}');""".format(user_email, user_password, user_name, role, 0)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        return user_name

    def get_user(self, email):
        """This gets a specific user values"""
        query = """ SELECT * FROM users where email='{}';""".format(email)
        cur = self.con.cursor()
        cur.execute(query)
        user = cur.fetchone()
        return user
