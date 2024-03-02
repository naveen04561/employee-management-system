from flask_sqlalchemy import SQLAlchemy
from models.root_db import db
from enum import Enum


class CategoryEnum(Enum):
    TECHNICAL = 'technical'
    COWORKER = 'coworker'
    COMPANY_RISK = 'company_risk'


class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True)
    # employees = db.relationship('Employee', backref='position_info')
    
    time_stamp = db.Column(db.DateTime)
    category = db.Column(db.Enum(CategoryEnum, values_callable=lambda x: [str(role.value) for role in CategoryEnum]))
    content = db.Column(db.String(2000))
    created_by = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    is_acknowledged = db.Column(db.Boolean)
    creating_employee = db.relationship('Employee', backref='ticket_list', foreign_keys=[created_by])