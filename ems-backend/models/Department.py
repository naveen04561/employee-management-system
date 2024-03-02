from models.root_db import db
from enum import Enum



class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True)
    # employees = db.relationship('Employee', back_populates='department')
    name = db.Column(db.String(100))
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True)
    

    