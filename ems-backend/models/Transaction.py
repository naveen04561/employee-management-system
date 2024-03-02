from flask_sqlalchemy import SQLAlchemy
from models.root_db import db


class Transaction(db.Model):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.DateTime)
    recipient_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    TDS = db.Column(db.Float)
    net_amount = db.Column(db.Float)
    is_successful = db.Column(db.Boolean)
    recipient = db.relationship('Employee', backref='transactions', foreign_keys=[recipient_id])
    