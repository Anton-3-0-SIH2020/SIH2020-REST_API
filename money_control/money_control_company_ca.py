from configparser import ConfigParser
import psycopg2

configure = ConfigParser()
configure.read("secret.ini")

DATABASE = configure.get("POSTGRES", "DATABASE")
USER = configure.get("POSTGRES", "USER")
PASSWORD = configure.get("POSTGRES", "PASSWORD")
HOST = configure.get("POSTGRES", "HOST")
PORT = configure.get("POSTGRES", "PORT")

def company_ca(symbol):
    connection = psycopg2.connect(
        user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE,
    )
    cursor = connection.cursor()

    sym=symbol.strip()

    cursor.execute('SELECT * FROM mc_ca WHERE company_name = ?',(symbol,))
    ca_array=[]
    for data in c:
        corporate_action={
            'company_name':data[1],
            'purpose':data[2],
            'anouncement':data[3],
            'record_date':data[4],
            'ex-date':data[5],
            'bc_start_date':'None',
            'bc_end_date':'None',
            'nd_start_date':'None',
            'nd_end_date':'None',
            'actual_payment_date':'None'
        }
        ca_array.append(corporate_action)
    connection.commit()
    cursor.close()
    conn.close()
    return (ca_array)