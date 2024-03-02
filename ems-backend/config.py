import os
from datetime import timedelta
import sqlalchemy as sa

connection_url = sa.engine.URL.create(
    drivername="mysql",
    username="root",
    password="",
    host="localhost",
    database="employee_management_system",
)
print(connection_url)

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@localhost:3306/employee_management_system'
# SQLALCHEMY_DATABASE_URI = connection_url

SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = 'sessions'
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)