from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models.root_db import Model
import enum



class RoleEnum(enum.Enum):
    REGULAR = 'regular'
    MANAGER = 'manager'
    ADMIN = 'admin'
    ACCOUNTANT = 'accountant'
    

class Employee(Model):
    __tablename__ = 'employee'
    employee_id = Column(Integer, primary_key=True)
    password = Column(String(100))
    f_name = Column(String(100))
    m_name = Column(String(100))
    l_name = Column(String(100))
    phone_number = Column(String(10))
    bank_account_num = Column(String(100))
    bank_name = Column(String(100))
    bank_IFSC_code = Column(String(100))
    is_terminated = Column(Boolean)
    role_id = Column(Enum(RoleEnum, values_callable=lambda x: [e.value for e in x]))
    # department works in relationship
    department_id = Column(Integer, ForeignKey('department.department_id'), nullable=True)
    # department = relationship('Department', back_populates='employees', foreign_keys=[department_id])
    # manager works for relationship
    manager_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=True)
    # employees_under = relationship('Employee', backref='manager', remote_side=employee_id)
    manager = relationship('Employee', remote_side=[employee_id])
    # project works on relationship
    project_id = Column(Integer, ForeignKey('project.project_id'), nullable=True)
    # works_on = relationship('Project', back_populates='employees', foreign_keys=[project_id])
    position = Column(String(9), ForeignKey('salary_structure.position_code'))
    position_info = relationship('Salary_structure', backref='employees')

    # department_under = relationship('Department', back_populates='manager')
    # project_under = relationship('Project', back_populates='manager')
    

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