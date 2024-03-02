from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models.root_db import Model
import enum


class AStatusEnum(enum.Enum):
    PRESENT = 'present'
    ABSENT = 'absent'
    LEAVE = 'leave'

class Attendance(Model):
    __tablename__ = 'attendance'
    attendance_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'), primary_key=True)
    date = Column(DateTime)
    status = Column(Enum(AStatusEnum, values_callable=lambda x: [e.value for e in x]))
    employee = relationship('Employee', backref='attendance_list', foreign_keys=[employee_id])
    