from datetime import datetime
from configparser import ConfigParser
import psycopg2

configure = ConfigParser()
configure.read("secret.ini")

DATABASE = configure.get("POSTGRES", "DATABASE")
USER = configure.get("POSTGRES", "USER")
PASSWORD = configure.get("POSTGRES", "PASSWORD")
HOST = configure.get("POSTGRES", "HOST")
PORT = configure.get("POSTGRES", "PORT")


def add_as_subscriber(request):
    json_req = request.get_json()

    uid = json_req.get('uid', None)
    if uid is None:
        return {'status': "UID not provided"}
    email = json_req.get('email', None)
    if email is None:
        return {'email': "Email Address not provided"}
    connection = psycopg2.connect(
        user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE,
    )
    cursor = connection.cursor()
    query = "CREATE TABLE IF NOT EXISTS subscriber_list(uid integer PRIMARY KEY, email text)"
    cursor.execute(query)
    connection.commit()
    cursor.execute(
        "SELECT * FROM subscriber_list WHERE uid = '{}' LIMIT 1".format(uid,))
    ca_array = []
    # Query exists
    if cursor.fetchone() is not None:
        cursor.execute(
            "DELETE FROM subscriber_list WHERE uid = '{}'".format(uid,))
        connection.commit()
        cursor.close()
        connection.close()
        return {'status': 'User removed from subscriber list'}
    else:
        cursor.execute(
            "INSERT INTO subscriber_list VALUES (%s, %s)", (uid, email))
        connection.commit()
        cursor.close()
        connection.close()
        return {'status': 'User inserted from subscriber list'}
