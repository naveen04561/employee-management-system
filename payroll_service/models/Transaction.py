from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models.root_db import Model


class Transaction(Model):
    __tablename__ = 'transaction'
    transaction_id = Column(Integer, primary_key=True)
    time_stamp = Column(DateTime)
    recipient_id = Column(Integer, ForeignKey('employee.employee_id'))
    TDS = Column(Float)
    net_amount = Column(Float)
    is_successful = Column(Boolean)
    recipient = relationship('Employee', backref='transactions', foreign_keys=[recipient_id])
    