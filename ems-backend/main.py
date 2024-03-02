from flask import Flask, session
from config import DEBUG
from models.root_db import db
from routes.employee_bp import employee_bp
from routes.auth_bp import auth_bp
from routes.admin_bp import admin_bp
from routes.manager_bp import manager_bp
from routes.accountant_bp import accountant_bp
from flask_cors import CORS
from flask_session import Session 
from flask_jwt_extended import JWTManager


# from flask_session import Session 

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config.from_object('config')

db.init_app(app)
JWTManager(app)
sess = Session(app)
db.echo = True
app.register_blueprint(employee_bp, url_prefix='/employees')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(manager_bp, url_prefix='/manager')
app.register_blueprint(accountant_bp, url_prefix='/accountant')

@app.route('/')
def index():
    return 'Hello'

if __name__ == '__main__':
    app.run(debug=DEBUG)