from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models.root_db import Model
import enum

class StatusEnum(enum.Enum):
    INPROGRESS = 'inprogress'
    DONE = 'done'

class Promotion(Model):
    __tablename__ = 'promotion'
    promotion_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    reason = Column(String)
    recommended_by = Column(Integer, ForeignKey('employee.employee_id'))
    recommended_for = Column(String(9))
    status = Column(Enum(StatusEnum, values_callable=lambda x: [e.value for e in x]))
    # employee_recommended = relationship('Employee', backref='recommended_list', foreign_keys=[employee_id])
    # manager_recommending = relationsip('Employee', backref='recommended_list', foreign_keys=[recommended_by])
    