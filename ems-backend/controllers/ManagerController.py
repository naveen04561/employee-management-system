from flask import jsonify, request, session, Response
from models.root_db import db
from models.Employee import Employee
from models.Salary_structure import Salary_structure
from models.Department import Department
from models.Promotion import Promotion, StatusEnum as PromotionStatusEnum
from models.Leave import Leave, StatusEnum
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from uuid import uuid4
import json

class ManagerController:
    def check_is_manager(self):
        if session.get('employee_id') is None or session.get('role') != 'manager':
            return True
        else:
            return False

    def getLeaveRequests(self):
        if not self.check_is_manager():
            return Response(
                "Authorization error: You are not a manager", 
                403
            )
        identity = get_jwt_identity()
        leaves_request = Leave.query.all()
        leaves_request_list = []
        for leave in leaves_request:
            if leave.employee_id == identity.get('employee_id'):
                continue
            if leave.status.value == StatusEnum.PENDING.value:
                leave_dict = {
                    "leave_id": leave.leave_id, 
                    "employee_id": leave.employee_id, 
                    "reason": leave.reason, 
                    "applied_date":leave.applied_date,
                    "start_date": leave.start_date,
                    "end_date": leave.end_date,
                    "status": leave.status.value,
                    "approved_by": leave.approved_by
                }
                leaves_request_list.append(leave_dict)

        return jsonify({
            "status": "FETCHED LEAVES REQUEST SUCCESSFULLY", 
            "leaves_request_list": leaves_request_list
        })

    def approveLeave(self):
        if not self.check_is_manager():
            return Response(
                "Authorization error: You are not a manager", 
                403
            )
        req = request.get_json()
        leave_approval_decision = req['leave_approval_decision']
        leave_to_approve = Leave.query.filter_by(leave_id=req['leave_id']).first()
        print(leave_to_approve)
        for status in StatusEnum:
                if status.value == req['leave_approval_decision']:
                    leave_to_approve.status = status
                    break
        db.session.add(leave_to_approve)
        db.session.commit()
        return jsonify({
            "status": f"Leave is {leave_approval_decision}", 
            "has_approved_leave": True
        })
    
    def recommendForPromotion(self):
        if not self.check_is_manager():
            return Response(
                "Authorization error: You are not a manager", 
                403
            )
        try:
            req = request.get_json()
            promotion = Promotion()
            promotion.employee_id = req['employee_id']
            promotion.promotion_id = (uuid4().int) % (2147483647)
            promotion.reason = req['reason']
            promotion.recommended_by = req['recommended_by']
            promotion.recommended_for = req['recommended_for']
            print("Recommended for ", req['recommended_for'])
            promotion.status = PromotionStatusEnum.INPROGRESS
            db.session.add(promotion)
            db.session.commit()
            return jsonify({
                "status": "Recommended for Promotion successfully", 
                "is_recommended": True
            })
        except Exception as e:
            return Response(f"Some error: {e}", 500)

    def assignProject(self):
        if not self.check_is_manager():
            return Response(
                "Authorization error: You are not a manager", 
                403
            )
        req = request.get_json()
        emp = Employee.query.filter_by(employee_id=req['emp_id']).first()
        emp.project_id = req['project_id']
        db.session.add(emp)
        db.session.commit()
        return jsonify({
                "status": "Assigned Project successfully", 
                "is_assigned": True
            })