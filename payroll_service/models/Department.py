from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models.root_db import Model




class Department(Model):
    __tablename__ = 'department'
    department_id = Column(Integer, primary_key=True)
    # employees = relationship('Employee', back_populates='department')
    name = Column(String(100))
    manager_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=True)
    

    