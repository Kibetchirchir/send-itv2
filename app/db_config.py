import psycopg2

url = "dbname='send_it' host='localhost' port='5432' user='postgres' password='v0k3ch!97'"


def connection(url):
    """connection to our database"""
    con = psycopg2.connect(url)
    return con


def init_db():
    """This is the initialization of our db"""
    con = connection(url)
    return con


def create_tables():
    """This is the function to create our tables"""
    conn = connection(url)
    cursor = conn.cursor()
    queries = tables()
    for query in queries:
        cursor.execute(query)
    conn.commit()


def destroy_tables():
    """this endpoint is used to destroy our tables"""
    conn = connection(url)
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE users, parcels, reset_passwords;""")
    conn.commit()


def tables():
    """queries for our database to create our tables"""
    users = """ CREATE TABLE IF NOT EXISTS users(
            user_id serial PRIMARY KEY,
            email VARCHAR(96) UNIQUE,
            password VARCHAR(48) NOT NULL,
            user_name VARCHAR(250),
            is_admin BOOL NOT NULL DEFAULT '0',
            is_active BOOL NOT NULL DEFAULT '0'
            );
            """

    parcels = """ CREATE TABLE IF NOT EXISTS parcels(
            parcel_id serial PRIMARY KEY,
            user_id serial NOT NULL,
            parcel_type VARCHAR(100),
            recipient_name VARCHAR(100) NOT NULL,
            recipient_number int,
            weight INT NOT NULL,
            destination_from VARCHAR NOT NULL,
            destination_to VARCHAR(250) NOT NULL,
            status VARCHAR(48) NOT NULL DEFAULT 'not_picked',
            longitude VARCHAR(6) NOT NULL,
            latitude VARCHAR(6) NOT NULL,
            price int NOT NULL,
            FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            );
            """

    reset_password = """ CREATE TABLE IF NOT EXISTS reset_passwords(
                     token_id serial PRIMARY KEY,
                     user_id serial NOT NULL,
                     token VARCHAR(250),
                     FOREIGN KEY (user_id)
                             REFERENCES users (user_id)
                             ON UPDATE CASCADE ON DELETE CASCADE                                          
                     );"""
    queries = [users, parcels, reset_password]
    return queries