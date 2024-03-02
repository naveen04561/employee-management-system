from multiprocessing import managers
from flask import Blueprint, session, request
from controllers.ManagerController import *
from flask_jwt_extended import jwt_required

manager = ManagerController()


manager_bp = Blueprint('manager_bp', __name__)

manager_bp.route('/leaves_list', methods=['GET'])(jwt_required()(manager.getLeaveRequests))
manager_bp.route('/approve_leave', methods=['POST'])(manager.approveLeave)
manager_bp.route('/recommend_promotion', methods=['POST'])(manager.recommendForPromotion)
manager_bp.route('/assign_project', methods=['POST'])(manager.assignProject)