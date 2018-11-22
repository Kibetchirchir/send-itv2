"""Docstring This class for our parcel model"""
from ....db_config import init_db


class ParcelModel:
    """"This is the class parcel model for testing model"""

    def __init__(self):
        """initialzation for our data"""
        self.con = init_db()

    def add_parcel(self, data, user_id):
        """This method adds parcels to our parcels"""
        parcel_type = data['parcel_type']
        dest = data['Dest']
        dest_from = data['Dest_from']
        status = data['status']
        recepient_name = data['recepient_name']
        recepient = data['recepient_number']
        weight = data['weight']
        price = 20
        query = """ INSERT INTO parcels(user_id, parcel_type, recipient_name, recipient_number, weight, 
                    destination_from,destination_to, status,price )
                     values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', 
                     '{}', '{}');""".format(user_id, parcel_type, recepient_name, recepient, weight, dest_from,
                                            dest, status, price)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        return data