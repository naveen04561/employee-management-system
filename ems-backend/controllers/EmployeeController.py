import sys
from flask import jsonify, request, Response
from flask_jwt_extended import get_jwt_identity
from models.root_db import db
from models.Employee import Employee
from models.Salary_structure import Salary_structure
from models.Department import Department
from models.Leave import Leave, StatusEnum
from models.Ticket import Ticket, CategoryEnum
from models.Transaction import Transaction
from flask_sqlalchemy import SQLAlchemy


from datetime import datetime
from uuid import uuid4
import json



# query for details required on the dashboard
# first_name, middle_name, last_name, employee_id, contact_number, department_name, 
# manager_name, position, bank account number, ifsc code bank name
class EmployeeController:
    def __init__(self):
        pass
    def check_is_employee(self):
        identity = get_jwt_identity()
        if identity.get('employee_id') is None or identity.get('role') not in ['regular', 'admin', 'manager', 'accountant']:
            return False
        else:
            return True



    def getDetails(self):
        if not self.check_is_employee():
            return Response(
                "Authorization error: You are not an employee", 
                403
            )
        identity = get_jwt_identity()
        _employee_id = identity.get('employee_id')
        _emp = Employee.query.filter_by(employee_id=_employee_id).first()
        print(_emp.f_name)
        if _emp is None:
            return Response(
                "Some error occurred. Cannot find record for employee", 
                500
            )
        department_info = db.session.query(Employee, Department).filter(Employee.department_id == Department.department_id).filter(Employee.employee_id == _emp.employee_id).first()
        if department_info is not None:
            department_info = department_info[1]
        
        
        
        print("PRRRRRRRRINTT", _emp.manager, _emp.position_info.employees)
        response = {
           "personal": {

                "first_name": _emp.f_name, 
                "middle_name": _emp.m_name, 
                "last_name": _emp.l_name,
                "employee_id": _emp.employee_id, 
                "phone_number": _emp.phone_number
           }, 
           "bank_details": {
                "bank_account_num": _emp.bank_account_num, 
                "bank_IFSC_code": _emp.bank_IFSC_code
           }, 
           "department_name": department_info.name if department_info != None else "", 
           "role_id": str(_emp.role_id.value) if _emp.role_id != None else "regular",
           "manager_name": "" if _emp.manager == None else f"{_emp.manager.f_name}", 
           "position": _emp.position_info.position


        }
        if department_info is not None:
            response['department_info'] = department_info.name
        
        if department_info is not None:
            response["manager_name"] = "" if _emp.manager == None else f"{_emp.manager.f_name}", 
            
        return jsonify(response)

    def _validateLeaveInfo(self, start_date, end_date, reason):
        try:
            start_dt = datetime.strptime(start_date, "%d-%m-%Y")
            end_dt = datetime.strptime(end_date, "%d-%m-%Y")

            if start_dt > end_dt:
                return False, "INVALID DATES GIVEN"
            return True, "SUCCESSFUL"
        except Exception as e:
            return False, "INVALID DATE FORMAT"

    def changePassword(self):
        if not self.check_is_employee():
            return Response(
                "Authorization error: You are not an employee", 
                403
            )
        identity = get_jwt_identity()
        req = request.get_json()
        _employee_id = identity.get('employee_id')
        print(_employee_id)
        _emp = Employee.query.filter_by(employee_id=_employee_id).first()
        _emp.password = req['new_password']
        db.session.add(_emp)
        db.session.commit()


    def applyForLeave(self):
        if not self.check_is_employee():
            return Response(
                "Authorization error: You are not an employee", 
                403
            )
        lv = Leave()
        lv.leave_id = (uuid4().int)%(10*10)
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']
        valid, status = self._validateLeaveInfo(start_date, end_date, reason)
        if not valid:
            return jsonify({
                "status": status, 
                "leave_requested": False
            })
        lv.applied_date = datetime.now()
        lv.start_date = datetime.strptime(start_date, "%d-%m-%Y")
        lv.end_date = datetime.strptime(end_date, "%d-%m-%Y")
        lv.reason = reason
        lv.status = StatusEnum.PENDING
        identity = get_jwt_identity()
        lv.employee_id = identity.get('employee_id')
        db.session.add(lv)
        db.session.commit()
        
        return jsonify({
            "status": status, 
            "leave_requested": True, 
            "leave_id": lv.employee_id
        })

        
    def _validateTicketInfo(self, category: str):
        
        for cat in list(CategoryEnum):
            if category == cat.value:
                return True, "VALID TICKET"
        return False, "INVALID TICKET CATEGORY"

    def raiseTicket(self):
        if not self.check_is_employee():
            return Response(
                "Authorization error: You are not an employee", 
                403
            )

        identity = get_jwt_identity()
        _employee_id = identity.get('employee_id')
        category = request.form['category']
        content = request.form['content']
        
        validTicket, status = self._validateTicketInfo(category)
        if not validTicket:
            return jsonify({
                "status": status, 
                "ticket_added": False, 
            })
        
        _category = None
        for cat in CategoryEnum:
            if cat.value == category:
                _category = cat

        newTicket = Ticket()
        newTicket.ticket_id = (uuid4().int)%(10*10)
        newTicket.category = _category
        newTicket.content = content
        newTicket.created_by = _employee_id
        newTicket.is_acknowledged = False
        db.session.add(newTicket)
        db.session.commit()
        return jsonify({
            "status": status, 
            "ticket_added": True, 
            "ticket_id": newTicket.ticket_id
        })
        
    def seeTicketInfo(self):
        if not self.check_is_employee():
            return Response(
                "Authorization error: You are not an employee", 
                403
            )
        identity = get_jwt_identity()
        _employee_id = identity.get('employee_id')
        emp = Employee.query.filter_by(employee_id=_employee_id).one()
        if emp is None:
            return Response(
                "Some error occurred. Cannot find record for employee", 
                500
            )
        tickets = emp.ticket_list
        tickets_list = []
        for ticket in tickets:
            ticket_dict = {
                "ticket_id": ticket.ticket_id, 
                "category": ticket.category.name, 
                "content": ticket.content
            }
            tickets_list.append(ticket_dict)
        
        return jsonify({
            "status": "SUCCESSFUL", 
            "ticket_list": tickets_list
        })



    def seeLeaveInfo(self):
        if not self.check_is_employee():
            return Response(
                "Authorization error: You are not an employee", 
                403
            )
        identity = get_jwt_identity()
        _employee_id = identity.get('employee_id')
        leaves = Leave.query.filter_by(employee_id=_employee_id).order_by(Leave.start_date).all()
        leaves_list = []
        for leave in leaves:
            print(leave.__dict__)
            leave_dict = {
                "applied_date": leave.applied_date, 
                "start_date": leave.start_date.strftime("%d-%m-%Y"), 
                "end_date": leave.end_date.strftime("%d-%m-%Y"), 
                "reason": leave.reason, 
                "leave_status": json.dumps(leave.status, default=lambda x: x.name), 
            }
            if leave.approved_by is not None:
                leave_dict["approved_by"] = f"{leave.approving_manager.f_name} {leave.approving_manager.m_name} {leave.approving_manager.l_name}"
            
            leaves_list.append(leave_dict)
        return jsonify({
            "status": "SUCCESSFUL", 
            "leave_list": leaves_list
        })

    def checkTransactionHistory(self):
        if not self.check_is_employee():
            return Response(
                "Authorization error: You are not an employee", 
                403
            )
        identity = get_jwt_identity()
        _employee_id = identity.get('employee_id')
        emp = Employee.query.filter_by(employee_id=_employee_id).first()
        if emp is None:
            return Response(
                "Some error occurred. Cannot find record for employee", 
                500
            )
        transactions = emp.transactions
        transaction_list = []
        for transaction in transactions:
            transaction_dict = {
                "transaction_id": transaction.transaction_id, 
                "timestamp": transaction.time_stamp, 
                "TDS": transaction.TDS, 
                "net_amount": transaction.net_amount
            }
            transaction_list.append(transaction_dict)
        
        return jsonify({
            "status": "SUCCESS FETCH OF TRANSACTIONS", 
            "transactions": transaction_list
        })
