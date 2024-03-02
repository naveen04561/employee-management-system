from flask_sqlalchemy import SQLAlchemy
from models.root_db import db
from enum import Enum


class AStatusEnum(Enum):
    PRESENT = 'present'
    ABSENT = 'absent'
    LEAVE = 'leave'

class Attendance(db.Model):
    __tablename__ = 'attendance'
    attendance_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
    date = db.Column(db.DateTime)
    status = db.Column(db.Enum(AStatusEnum, values_callable=lambda x: [str(role.value) for role in AStatusEnum]))
    employee = db.relationship('Employee', backref='attendance_list', foreign_keys=[employee_id])
    