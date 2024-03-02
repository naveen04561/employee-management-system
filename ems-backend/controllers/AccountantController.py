from flask import jsonify, request, session, Response
from models.root_db import db
from models.Transaction import Transaction
from config import SQLALCHEMY_DATABASE_URI
import sqlalchemy as db
from sqlalchemy.engine import result
from datetime import datetime

# connection_url = db.engine.URL.create(
#     drivername="mysql",
#     username="root",
#     password="Naveen@123",
#     host="localhost",
#     database="employee_management_system",
# )

def calculateExpenditure():
        engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
        meta_data = db.MetaData(bind=engine)
        db.MetaData.reflect(meta_data)
        TRANSACTIONS = meta_data.tables['transaction']

        query = db.select([
            TRANSACTIONS.c.time_stamp,
            db.func.sum(TRANSACTIONS.c.net_amount)
        ]).group_by(db.func.month(TRANSACTIONS.c.time_stamp))

        result = engine.execute(query).fetchall()
        final_result = []
        for record in result:
            d = {}
            d['net_amount'] = record[1]
            d['month'] = str(record[0])[0:7]
            final_result.append(d)
        return final_result

class AccountantController:
    def viewExpenditure(self):
        expenditure_list = calculateExpenditure()
        return jsonify({
            "status": "FETCHED EXPENDITURE DETAILS SUCCESSFULLY", 
            "expenditure_list": expenditure_list
        })

