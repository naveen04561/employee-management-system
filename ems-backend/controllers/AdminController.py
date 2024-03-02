from flask import jsonify, request, session, Response
from flask_jwt_extended import get_jwt_identity
from models.root_db import db
from models.Employee import Employee, RoleEnum
from models.Salary_structure import Salary_structure
from models.Department import Department
from models.Leave import Leave, StatusEnum
from models.Ticket import Ticket, CategoryEnum
from models.Transaction import Transaction
from models.Promotion import Promotion, StatusEnum
from models.Project import Project
from flask_sqlalchemy import SQLAlchemy

from controllers.sendSMS import sendPassword
from datetime import datetime
from uuid import uuid4
import json



# query for details required on the dashboard
# first_name, middle_name, last_name, employee_id, contact_number, department_name, 
# manager_name, position, bank account number, ifsc code bank name
class AdminController:
    
    def check_is_admin(self):
        identity = get_jwt_identity()
        if identity.get('employee_id') is None or identity.get('role') != 'admin':
            
            return False
        else:
            print(identity.get('employee_id'), identity.get('role'))
            return True
        
    def addEmployee(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        req = request.get_json()
        print(req)
        # try:
        emp = Employee()
        emp.employee_id = (uuid4().int) % (2147483647)
        emp.f_name = req['first_name']
        emp.m_name = req['middle_name']
        emp.l_name = req['last_name']
        emp.password = str(uuid4())
        emp.phone_number = req['phone_number'] # to be verified

        emp.bank_account_num = req['bank_account_number']
        emp.bank_name = req['bank_name']
        emp.bank_IFSC_code = req['bank_ifsc_code']
        emp.is_terminated = False
        
        _role = None
        for role in RoleEnum:
            print(role.value)
            if role.value == req['role_id']:
                _role = role

        emp.role_id = _role
        emp.department_id = req['department_id']
        emp.project_id = req['project_id']
        if req['project_id'] is None:
            emp.manager_id = None
        else:
            proj = Project.query.filter_by(project_id=req['project_id']).first()
            manager_id = proj.manager_id
            emp.manager_id = manager_id
            
        emp.position = req['position']
        status, message = sendPassword(emp.employee_id, emp.password, emp.phone_number)
        if status is False:
            raise Exception(message)
        db.session.add(emp)
        db.session.commit()
        return jsonify({
            "status": "Created new employee successfully", 
            "is_inserted": True, 
            "is_activated": False, 
            "employee_id": emp.employee_id
        })
        # except Exception as e:
        #     return Response(f"Some error while inserting data: {e}", 500)


    def getEmployeeDetails(self, employee_id):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        req = request.get_json()
        emp_id = employee_id
        emp = Employee.query.filter_by(employee_id=emp_id, is_terminated=False).first()
        return jsonify({
            'employee_id': emp.employee_id,
            'f_name': emp.f_name,
            'm_name': emp.m_name,
            'l_name': emp.l_name,
            'phone_number': emp.phone_number[3: ],
            'bank_account_num': emp.bank_account_num,
            'bank_name': emp.bank_name,
            'bank_IFSC_code': emp.bank_IFSC_code,
            'is_terminated': emp.is_terminated,
            'role_id': emp.role_id.value,
            'department_id': emp.department_id,
            'manager_id': emp.manager_id,
            'project_id': emp.project_id,
            'position': emp.position
        })

    def editEmployee(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        req = request.get_json()
        # try:
        emp_id = req['employee_id']
        emp = Employee.query.filter_by(employee_id=emp_id).one()
        emp.f_name = req['first_name']
        emp.m_name = req['middle_name']
        emp.l_name = req['last_name']
        emp.phone_number = req['phone_number'] # to be verified
        emp.bank_account_num = req['bank_account_number']
        emp.bank_name = req['bank_name']
        emp.bank_IFSC_code = req['bank_ifsc_code']
        
        _role = None
        for role in RoleEnum:
            if role.value == req['role_id']:
                _role = role

        emp.role_id = _role
        emp.department_id = req['department_id']
        emp.project_id = req['project_id']
        proj = Project.query.filter_by(project_id=emp.project_id).first()
        emp.manager_id = proj.manager_id
        db.session.add(emp)
        db.session.commit()
        return jsonify({
            "status": f"Edited employee {emp.employee_id} successfully", 
            "is_inserted": True
        })
        # except Exception as e:
        #     return Response(f"Some error while editing data: {e}", 500)
    
    def terminateEmployee(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        req = request.get_json()

        try:
            emp_id = req['employee_id']
            emp = Employee.query.filter_by(employee_id=emp_id).one()
            emp.is_terminated = True
            db.session.add(emp)
            db.session.commit()
            return jsonify({
                "status": f"Terminated employee {emp.employee_id} successfully", 
                "is_terminated": True
            })
        except Exception as e:
            return Response("Some error while terminating employee", 500)

    def getRecommendationList(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        promotion_requests = Promotion.query.all()
        promotion_request_list = []
        for promotion in promotion_requests:
            promotion_dict = {
                "promotion_id": promotion.promotion_id, 
                "employee_id": promotion.employee_id, 
                "reason": promotion.reason, 
                "recommended_by": promotion.recommended_by, 
                "recommended_for": promotion.recommended_for, 
                "status": promotion.status.value
            }
            promotion_request_list.append(promotion_dict)

        return jsonify({
            "status": "FETCHED RECOMMENDATIONS SUCCESSFULLY", 
            "recommendation_list": promotion_request_list
        })

    def changeEmployeePosition(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        req = request.get_json()
        # try:
        emp_id = req['employee_id']
        manager_id = req['recommended_by']
        position_code = req['recommended_for']
        promotion_request = Promotion.query.filter_by(employee_id=emp_id, recommended_by=manager_id, status=StatusEnum.INPROGRESS).first()
        if promotion_request is None:
            raise Exception("No promotion request")
        

        emp = Employee.query.filter_by(employee_id=emp_id).one()
        if emp.manager_id != promotion_request.recommended_by:
            raise Exception("Recommender is not employee's manager")

        emp.position = position_code
        emp.manager_id = None
        promotion_request.status = StatusEnum.DONE
        db.session.add(promotion_request)
        db.session.add(emp)
        db.session.commit()
        return jsonify({
            "status": f"Changed postion of employee {emp.employee_id} successfully", 
            "has_changed_position": True
        })
        # except Exception as e:
        #     return Response(f"Some error while changing employee position {e}", 500)

    def getPositionInfo(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        positions = Salary_structure.query.all()
        position_list = []
        for position in positions:
            position_dict = {
                "position_code": position.position_code, 
                "position": position.position, 
                "monthly_salary": position.value
            }
            position_list.append(position_dict)
        return jsonify({
            "status": "SUCCESSFULLY FETCHED LIST OF POSITIONS", 
            "position_list": position_list
        })

    def reassignEmployeeProject(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        req = request.get_json()
    
        try:
            emp_id = req['employee_id']
            new_proj_id = req['new_project_id']
            emp = Employee.query.filter_by(employee_id=emp_id).one()
            proj = Project.query.filter_by(project_id=new_proj_id).one()
            emp.project_id = new_proj_id
            emp.manager_id = proj.manager_id
            db.session.add(emp)
            db.session.commit()
            return jsonify({
                "status": f"Terminated employee {emp.employee_id} successfully", 
                "is_terminated": True
            })
        except Exception as e:
            return Response("Some error while changing project", 500)


    def createProject(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        req = request.get_json()
        try:
            new_proj = Project()
            new_proj.name = req["name"]
            new_proj.project_id = uuid4()%(2147483647)
            projects = Project.query.filter_by(manager_id=req['manager_id']).all()
            if len(projects) > 0:
                raise Exception("Cannot assign manager to project as the manager is already occupied. First reassign the project with someone else and then assign")
                
            new_proj.manager_id = req["manager_id"]
            db.session.add(new_proj)
            db.session.commit()
            return jsonify({
                "status": f"Created project  successfully", 
                "is_created": True, 
                "project_id": new_proj.project_id
            })
        except Exception as e:
            return Response(f"Some error while creating new project: {e}", 500)


    def getTickets(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        tickets = Ticket.query.all()
        ticket_list = []
        for ticket in tickets:
            ticket_dict = {
                "ticket_id": ticket.ticket_id, 
                "timestamp": ticket.time_stamp, 
                "category": ticket.category.value, 
                "content": ticket.content, 
                "created_by": ticket.created_by
            }
            ticket_list.append(ticket_dict)
        return jsonify({
            "status": "SUCCESSFULLY FETCHED ALL TICKETS", 
            "ticket_list": ticket_list
        })


    def getProjectInfo(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        projects = Project.query.all()
        project_list = []
        for project in projects:
            project_dict = {
                "project_id": project.project_id, 
                "name": project.name, 
                "manager_id": project.manager_id
            }
            project_list.append(project_dict)

        return jsonify({
            "status": "SUCCESSFULLY FETCHED ALL PROJECT DETAILS", 
            "project_list": project_list
        })
    
    def getManagerByProjectId(self, project_id):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        
        # req = request.get_json()
        # project_id = req["project_id"]
        print(project_id)
        emp_proj = db.session.query(Employee, Project).filter(Project.project_id == project_id).filter(Employee.employee_id == Project.manager_id).first()

        if emp_proj is not None:
            emp = emp_proj[0]
            return jsonify({
                "status": "SUCCESSFULLY FETCHED PROJECT MANAGER", 
                "manager_name": f"{emp.f_name} {emp.m_name} {emp.l_name}"
            })
        else:
            return jsonify({
                "status": "NO RESULTS", 
                "manager_name": None
            })


    
    def getDepartmentInfo(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        departments = Department.query.all()
        department_list = []
        for department in departments:
            department_dict = {
                "department_id": department.department_id, 
                "name": department.name, 
                "manager_id": department.manager_id
            }
            department_list.append(department_dict)

        return jsonify({
            "status": "SUCCESSFULLY FETCHED ALL DEPARTMENT DETAILS", 
            "department_list": department_list
        })

    def reassignProjectManager(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        req = request.get_json()
        _manager_id = req['manager_id']
        _project_id = req['project_id']
        newManager = Employee.query.filter_by(employee_id=_manager_id)
        existing_manager_id = session.query(Project.manager_id).filter_by(project_id=_project_id)
        existingManager = Employee.query.filter_by(employee_id=existing_manager_id)
        project = Project.query.filter_by(project_id=_project_id).first()
        project.manager_id = _manager_id
        newManager.project_id = _project_id
        existingManager.project_id = None

        res = db.session.query(Project, Employee).\
            filter(Project.project_id == Employee.project_id).\
            filter(Employee.employee_id != newManager.employee_id).all()
        
        for  _, emp in res:
            emp.manager_id = newManager.employee_id
            db.session.add(emp)

        db.session.add(project)
        db.session.add(newManager)
        db.session.commit()


        
    def acknowledgeTicket(self):
        if not self.check_is_admin():
            return Response(
                "Authorization error: You are not an admin", 
                403
            )
        req = request.get_json()
        _ticket_id = req['ticket_id']
        ticket = Ticket.query.filter_by(ticket_id=_ticket_id)
        ticket.is_acknowledged = True
        db.session.add(ticket)
        db.session.commit()
