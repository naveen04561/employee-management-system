import re
import sys
from tabnanny import check
from venv import create
from flask import jsonify, request, session, Response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

from models.Employee import Employee
from controllers.verifySMS import *


class AuthController:
    def login(self):
        import json
        emp_id = request.form['id']
        password = request.form['password']
        emp = Employee.query.filter_by(employee_id=emp_id).first()
        if emp is not None and emp.password == password:
            if emp.is_terminated is False:
                identity_information = {
                    'employee_id': emp_id, 
                    'role': emp.role_id.value
                }
                # session['employee_id'] = emp_id
                session['role'] = emp.role_id.value
                access_token = create_access_token(identity=identity_information)
                return jsonify({
                    "status": "login successful", 
                    "access_token": access_token
                })
        else:
            return Response(
                "Unsuccessful login: Wrong username or password", 
                status=403
            )
        
        
        
    def verifyPhoneNumber(self):
        identity = get_jwt_identity()
        if identity['role'] != "admin":
            return Response(
                "Unauthorized access: Only admin can access this feature", 
                status=403
            )
        # for testing uncomment following 3 lines of code
        # return jsonify({
        #     "identity": identity
        # })
        req = request.get_json()
        phone_number = req['phone_number']
        return verify(phone_number)

    
    def checkVerificationCode(self):
        req = request.get_json()
        phone_number = req['phone_number']
        OTP = req["otp"]
        return checkVerify(OTP, phone_number)


