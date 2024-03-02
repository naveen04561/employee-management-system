from models.root_db import db
from enum import Enum



class RoleEnum(Enum):
    REGULAR = 'regular'
    MANAGER = 'manager'
    ADMIN = 'admin'
    ACCOUNTANT = 'accountant'
    

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    f_name = db.Column(db.String(100))
    m_name = db.Column(db.String(100))
    l_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(10))
    bank_account_num = db.Column(db.String(100))
    bank_name = db.Column(db.String(100))
    bank_IFSC_code = db.Column(db.String(100))
    is_terminated = db.Column(db.Boolean)
    role_id = db.Column(db.Enum(RoleEnum, values_callable=lambda x: [str(role.value) for role in RoleEnum]))
    # department works in relationship
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable=True)
    # department = db.relationship('Department', back_populates='employees', foreign_keys=[department_id])
    # manager works for relationship
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True)
    # employees_under = db.relationship('Employee', backref='manager', remote_side=employee_id)
    manager = db.relationship('Employee', remote_side=[employee_id])
    # project works on relationship
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=True)
    # works_on = db.relationship('Project', back_populates='employees', foreign_keys=[project_id])
    position = db.Column(db.String(9), db.ForeignKey('salary_structure.position_code'))
    position_info = db.relationship('Salary_structure', backref='employees')

    # department_under = db.relationship('Department', back_populates='manager')
    # project_under = db.relationship('Project', back_populates='manager')
    

    @property
    def serialize(self):
        return {
            'employee_id': self.employee_id,
            'f_name': self.f_name,
            'm_name': self.m_name,
            'l_name': self.l_name,
            'phone_number': self.phone_number,
            'bank_account_num': self.bank_account_num,
            'bank_name': self.bank_name,
            'bank_IFSC_code': self.bank_IFSC_code,
            'is_terminated': self.is_terminated,
            'role_id': self.role_id,
            'department_id': self.department_id,
            'manager_id': self.manager_id,
            'project_id': self.project_id,
            'position': self.position
        }