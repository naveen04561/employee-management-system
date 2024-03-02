from flask_sqlalchemy import SQLAlchemy
from models.root_db import db


class Payroll(db.Model):
    __tablename__ = 'payroll'
    run_id = db.Column(db.Integer, primary_key=True)
    # employees = db.relationship('Employee', backref='position_info')
    
    date = db.Column(db.DateTime)
    TDS_collected = db.Column(db.Float)