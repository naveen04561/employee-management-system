from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models.root_db import Model


class Payroll(Model):
    __tablename__ = 'payroll'
    run_id = Column(Integer, primary_key=True)
    # employees = relationship('Employee', backref='position_info')
    
    date = Column(DateTime)
    TDS_collected = Column(Float)