from flask_sqlalchemy import SQLAlchemy
from models.root_db import db


class Salary_structure(db.Model):
    __tablename__ = 'salary_structure'
    position_code = db.Column(db.Integer, primary_key=True)
    # employees = db.relationship('Employee', backref='position_info')
    position = db.Column(db.String(100))
    value = db.Column(db.Float)
    



    