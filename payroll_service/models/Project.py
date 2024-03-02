from flask_sqlalchemy import SQLAlchemy
from models.root_db import db
from enum import Enum


class Project(db.Model):
    __tablename__ = 'project'
    project_id = db.Column(db.Integer, primary_key=True)
    # employees = db.relationship('Employee', back_populates='works_on')
    name = db.Column(db.String(100))
    



    