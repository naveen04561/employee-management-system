from flask_sqlalchemy import SQLAlchemy
from models.root_db import db
from enum import Enum


class StatusEnum(Enum):
    PENDING = 'pending'
    GRANTED = 'granted'
    REJECTED = 'rejected'


class Leave(db.Model):
    __tablename__ = 'leaves'
    leave_id = db.Column(db.Integer, primary_key=True)
    applied_date = db.Column(db.DateTime)
    # employees = db.relationship('Employee', backref='position_info')
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    employee = db.relationship('Employee', backref='leaves', foreign_keys=[employee_id])
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.Enum(StatusEnum, values_callable=lambda x: [str(role.value) for role in StatusEnum]))
    reason = db.Column(db.String(1000))
    approved_by = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    approving_manager = db.relationship('Employee', backref='leave_request_list', foreign_keys=[approved_by])