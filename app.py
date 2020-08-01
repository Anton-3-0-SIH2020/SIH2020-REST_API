from flask import Flask, request, send_file, Response
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT
from boto3 import client
from configparser import ConfigParser
import json
import os

# BSE Imports
from bse import bse_latest_ca
from bse import bse_company_ca

# NSE Imports
from nse import nse_latest_ca
from nse import nse_company_ca

# MoneyControl Imports
from money_control import money_control_upcoming_ca
from money_control import money_control_company_ca

from user_email_subscribe import add_to_subscriber_list as subscribe

configure = ConfigParser()
configure.read("secret.ini")

ACCESS_KEY = configure.get("AWS", "ACCESS_KEY")
SECRET_KEY = configure.get("AWS", "SECRET_KEY")
BUCKET = configure.get("AWS", "BUCKET")
REGION = configure.get("AWS", "REGION")

app = Flask(__name__, static_url_path="/public", static_folder="public/")
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "Pratik"
api = Api(app)


def get_client():
    return client(
        's3',
        REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

# BSE Latest corporate action from the database(Server)


class LatestCA_BSE(Resource):
    def get(self):
        return {"latest_ca": bse_latest_ca.latest_ca(request)}


# BSE Particular company corporate action from historical data
class CompanyCA_BSE(Resource):
    def get(self, code):
        return {"ca": bse_company_ca.company_ca(code)}


# BSE PDF
class PDF_BSE(Resource):
    def get(self):
        KEY = 'Latest Corporate Actions BSE.pdf'
        s3 = get_client()
        file = s3.get_object(Bucket=BUCKET, Key=KEY)
        return Response(
            file['Body'].read(),
            mimetype='application/pdf',
            headers={"Content-Disposition": f"attachment;filename={KEY}"}
        )


# BSE CSV
class CSV_BSE(Resource):
    def get(self):
        KEY = 'Latest Corporate Actions BSE.csv'
        s3 = get_client()
        file = s3.get_object(Bucket=BUCKET, Key=KEY)
        return Response(
            file['Body'].read(),
            mimetype='application/csv',
            headers={"Content-Disposition": f"attachment;filename={KEY}"}
        )


# NSE Latest corporate action from the database
class LatestCA_NSE(Resource):
    def get(self):
        return {"latest_ca": nse_latest_ca.latest_ca(request)}


# NSE Particular company corporate action from historical data
class CompanyCA_NSE(Resource):
    def get(self, code):
        return {"ca": nse_company_ca.company_ca(code)}


# NSE PDF
class PDF_NSE(Resource):
    def get(self):
        KEY = 'Latest Corporate Actions NSE.pdf'
        s3 = get_client()
        file = s3.get_object(Bucket=BUCKET, Key=KEY)
        return Response(
            file['Body'].read(),
            mimetype='application/pdf',
            headers={"Content-Disposition": f"attachment;filename={KEY}"}
        )


# NSE CSV
class CSV_NSE(Resource):
    def get(self):
        KEY = 'Latest Corporate Actions NSE.csv'
        s3 = get_client()
        file = s3.get_object(Bucket=BUCKET, Key=KEY)
        return Response(
            file['Body'].read(),
            mimetype='application/csv',
            headers={"Content-Disposition": f"attachment;filename={KEY}"}
        )


# Money Control Latest corporate action from the database
class LatestCA_MC(Resource):
    def get(self):
        return {"latest_ca": money_control_upcoming_ca.latest_ca(request)}


# Money Control Particular company corporate action from historical data
class CompanyCA_MC(Resource):
    def get(self, code):
        return {"ca": money_control_company_ca.company_ca(code)}


# Money Control PDF
class PDF_MC(Resource):
    def get(self):
        KEY = 'Latest Corporate Actions MC.pdf'
        s3 = get_client()
        file = s3.get_object(Bucket=BUCKET, Key=KEY)
        return Response(
            file['Body'].read(),
            mimetype='application/pdf',
            headers={"Content-Disposition": f"attachment;filename={KEY}"}
        )


# BSE MC
class CSV_MC(Resource):
    def get(self):
        KEY = 'Latest Corporate Actions MC.csv'
        s3 = get_client()
        file = s3.get_object(Bucket=BUCKET, Key=KEY)
        return Response(
            file['Body'].read(),
            mimetype='application/csv',
            headers={"Content-Disposition": f"attachment;filename={KEY}"}
        )


class Subscribe(Resource):
    def post(self):
        return subscribe.add_as_subscriber(request)


api.add_resource(LatestCA_BSE, "/api/bse_latestca")
api.add_resource(CompanyCA_BSE, "/api/bse_companyca/<string:code>")
api.add_resource(PDF_BSE, "/download/bse_pdf")
api.add_resource(CSV_BSE, "/download/bse_csv")
api.add_resource(LatestCA_NSE, "/api/nse_latestca")
api.add_resource(CompanyCA_NSE, "/api/nse_companyca/<string:code>")
api.add_resource(PDF_NSE, "/download/nse_pdf")
api.add_resource(CSV_NSE, "/download/nse_csv")
api.add_resource(LatestCA_MC, "/api/mc_latestca")
api.add_resource(CompanyCA_MC, "/api/mc_companyca/<string:code>")
api.add_resource(PDF_MC, "/download/mc_pdf")
api.add_resource(CSV_MC, "/download/mc_csv")
api.add_resource(Subscribe, "/api/subscribe")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
