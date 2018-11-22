"""Docstring This class for our parcel model"""
from ....db_config import init_db
import uuid


class ParcelModel:
    """"This is the class parcel model for testing model"""

    def __init__(self):
        """initialzation for our data"""
        self.con = init_db()

    def add_parcel(self, data, user_id):
        """This method adds parcels to our parcels"""
        parcel_type = data['parcel_type']
        drop_off_location = data['drop_off_location']
        pick_up_location = data['pick_up_location']
        status = data['status']
        recepient_name = data['recepient_name']
        recepient = data['recepient_number']
        weight = data['weight']
        price = 20
        order_id = str(uuid.uuid1())
        query = """ INSERT INTO parcels(parcel_id, user_id, parcel_type, recipient_name, recipient_number, weight, 
                    destination_from,destination_to, status,price )
                     values ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', 
                     '{}', '{}');""".format(order_id, user_id, parcel_type, recepient_name, recepient, weight,
                                            pick_up_location,drop_off_location, status, price)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        data['order_no'] = order_id
        return data

