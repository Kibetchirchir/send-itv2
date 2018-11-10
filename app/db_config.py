import psycopg2

url = "dbname='pg' user='postgres' host='localhost' " + \
      "password='password'"


def connection(url):
    con = psycopg2.connect(url)
    return con


def init_db():
    con = connection(url)
    return con


def create_tables():
    conn = connection(url)
    cursor = conn.cursor()
    queries = tables()
    for query in queries:
        cursor.execute(query)
    conn.commit()


def destroy_tables():
    pass


def tables():
    users = """ CREATE TABLE IF NOT EXISTS users(
                user_id serial PRIMARY KEY,
                username VARCHAR(250) NOT NULL,
                email VARCHAR(96) UNIQUE,
                password VARCHAR(48) NOT NULL,
                status VARCHAR(48) NOT NULL DEFAULT 'pending delivery',
                user_role VARCHAR(48) NOT NULL DEFAULT 'user'
                );
                """

    parcels = """ CREATE TABLE IF NOT EXISTS parcels(
                parcel_id serial PRIMARY KEY,
                recipient VARCHAR(250) NOT NULL,
                weight INT NOT NULL,
                destination VARCHAR(250) NOT NULL,
                price INT NOT NULL
                );
                """
    query =[users, parcels]
    return query