from venv import create
from flask import Blueprint, session
from flask_jwt_extended import jwt_required
from controllers.EmployeeController import *


emp = EmployeeController()


employee_bp = Blueprint('employee_bp', __name__)
employee_bp.route('/', methods=['GET'])(jwt_required()(emp.getDetails))

employee_bp.route('/leaves_info', methods=['GET'])(jwt_required()(emp.seeLeaveInfo))
employee_bp.route('/raise_ticket', methods=['POST'])(jwt_required()(emp.raiseTicket))
employee_bp.route('/tickets_info', methods=['GET'])(jwt_required()(emp.seeTicketInfo))
employee_bp.route('/transaction_history', methods=['GET'])(jwt_required()(emp.checkTransactionHistory))
employee_bp.route('/apply_leave', methods=['POST'])(jwt_required()(emp.applyForLeave))


# employee_bp.route('/<int:employee_id>', methods=['DELETE'])(delete)