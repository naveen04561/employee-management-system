from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from models.root_db import Model

class Salary_structure(Model):
    __tablename__ = 'salary_structure'
    position_code = Column(Integer, primary_key=True)
    # employees = relationship('Employee', backref='position_info')
    position = Column(String(100))
    value = Column(Float)
    



    