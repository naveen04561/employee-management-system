from flask_sqlalchemy import SQLAlchemy
from models.root_db import db
from enum import Enum

class StatusEnum(Enum):
    INPROGRESS = 'inprogress'
    DONE = 'done'

class Promotion(db.Model):
    __tablename__ = 'promotion'
    promotion_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    reason = db.Column(db.String(500))
    recommended_by = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    recommended_for = db.Column(db.String(9))
    status = db.Column(db.Enum(StatusEnum, values_callable=lambda x: [str(role.value) for role in StatusEnum]))
    # employee_recommended = db.relationship('Employee', backref='recommended_list', foreign_keys=[employee_id])
    # manager_recommending = db.relationsip('Employee', backref='recommended_list', foreign_keys=[recommended_by])
    