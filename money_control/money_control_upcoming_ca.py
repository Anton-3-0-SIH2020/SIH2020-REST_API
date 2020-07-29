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

def latest_ca(request):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date:
        start_date = datetime.strptime(start_date, "%d-%b-%Y").strftime("%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%d-%b-%Y").strftime("%Y-%m-%d")
    company_name = request.args.get('company_name', '')
    connection = psycopg2.connect(
        user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE,
    )
    cursor = connection.cursor()
    query =""
    if start_date and end_date:
        query = f'SELECT * FROM latest_mc_ca WHERE company_name LIKE "%{company_name}%" AND ex_date BETWEEN date("{start_date}") and date("{end_date}")'
    elif start_date:
        query = f'SELECT * FROM latest_mc_ca WHERE company_name LIKE "%{company_name}%" AND ex_date >= date("{start_date}")'
    elif end_date:
        query = f'SELECT * FROM latest_mc_ca WHERE company_name LIKE "%{company_name}%" AND ex_date <= date("{end_date}")'
    else:
        query = f'SELECT * FROM latest_mc_ca WHERE company_name LIKE "%{company_name}%"'
    cursor.execute(query)
    ca_array=[]
    for data in c:
        corporate_action={
            'company_name':data[1],
            'purpose':data[2],
            'anouncement':data[3],
            'record_date':data[4],
            'ex-date':datetime.strptime(data[5], "%Y-%m-%d").strftime("%d-%b-%Y"),
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