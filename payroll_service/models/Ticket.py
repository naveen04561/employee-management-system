from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models.root_db import Model
from enum import Enum


class CategoryEnum(Enum):
    TECHNICAL = 'technical'
    COWORKER = 'coworker'
    COMPANY_RISK = 'company_risk'


class Ticket(Model):
    __tablename__ = 'ticket'
    ticket_id = Column(Integer, primary_key=True)
    # employees = relationship('Employee', backref='position_info')
    
    time_stamp = Column(DateTime)
    category = Column(Enum(CategoryEnum, values_callable=lambda x: [role.value for role in CategoryEnum]))
    content = Column(String(2000))
    created_by = Column(Integer, ForeignKey('employee.employee_id'))
    is_acknowledged = Column(Boolean)
    creating_employee = relationship('Employee', backref='ticket_list', foreign_keys=[created_by])