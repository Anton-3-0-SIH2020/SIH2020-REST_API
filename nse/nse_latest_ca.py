import psycopg2
from datetime import datetime
from configparser import ConfigParser

configure = ConfigParser()
configure.read("secret.ini")

DATABASE = configure.get("POSTGRES", "DATABASE")
USER = configure.get("POSTGRES", "USER")
PASSWORD = configure.get("POSTGRES", "PASSWORD")
HOST = configure.get("POSTGRES", "HOST")
PORT = configure.get("POSTGRES", "PORT")


def latest_ca(request):
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if start_date:
        start_date = datetime.strptime(
            start_date, "%d-%b-%Y").strftime("%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%d-%b-%Y").strftime("%Y-%m-%d")
    company_name = request.args.get("company_name", "")
    connection = psycopg2.connect(
        user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE,
    )
    cursor = connection.cursor()
    query = ""
    if start_date and end_date:
        query = f"SELECT * FROM latest_nse_ca WHERE company_name LIKE '%{company_name}%' AND ex_date BETWEEN date('{start_date}') and date('{end_date}')"
    elif start_date:
        query = f"SELECT * FROM latest_nse_ca WHERE company_name LIKE '%{company_name}%' AND ex_date >= date('{start_date}')"
    elif end_date:
        query = f"SELECT * FROM latest_nse_ca WHERE company_name LIKE '%{company_name}%' AND ex_date <= date('{end_date}')"
    else:
        query = (
            f"SELECT * FROM latest_nse_ca WHERE company_name LIKE '%{company_name}%'"
        )
    cursor.execute(query)
    ca_array = []
    for data in cursor:
        corporate_action = {
            "symbol": data[1],
            "company_name": data[2],
            "series": data[3],
            "face_value": data[4],
            "purpose": data[5],
            "ex_date": data[6].strftime("%d-%b-%Y"),
            "record_date": data[7],
            "bc_start_date": data[8],
            "bc_end_date": data[9],
        }
        ca_array.append(corporate_action)

    connection.commit()
    cursor.close()
    connection.close()
    return ca_array
