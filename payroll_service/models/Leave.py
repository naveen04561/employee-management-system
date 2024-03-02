from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models.root_db import Model
import enum


class StatusEnum(enum.Enum):
    PENDING = 'pending'
    GRANTED = 'granted'


class Leave(Model):
    __tablename__ = 'leaves'
    leave_id = Column(Integer, primary_key=True)
    applied_date = Column(DateTime)
    # employees = relationship('Employee', backref='position_info')
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    employee = relationship('Employee', backref='leaves', foreign_keys=[employee_id])
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Enum(StatusEnum, values_callable=lambda x: [e.value for e in x]))
    reason = Column(String(1000))
    approved_by = Column(Integer, ForeignKey('employee.employee_id'))
    approving_manager = relationship('Employee', backref='leave_request_list', foreign_keys=[approved_by])