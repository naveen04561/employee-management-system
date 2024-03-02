from flask import Blueprint, session, request
from flask_jwt_extended import jwt_required
from controllers.AdminController import *

admin = AdminController()


admin_bp = Blueprint('admin_bp', __name__)
admin_bp.route('/add', methods=['POST'])(jwt_required()(admin.addEmployee))
admin_bp.route('/edit/<employee_id>', methods=['GET'])(jwt_required()(admin.getEmployeeDetails))
admin_bp.route('/edit', methods=['POST'])(jwt_required()(admin.editEmployee))
admin_bp.route('/terminate', methods=['POST'])(jwt_required()(admin.terminateEmployee))
admin_bp.route('/change_position', methods=['GET'])(jwt_required()(admin.getRecommendationList))
admin_bp.route('/change_position', methods=['POST'])(jwt_required()(admin.changeEmployeePosition))
admin_bp.route('/create_project', methods=['POST'])(jwt_required()(admin.createProject))
admin_bp.route('/change_project', methods=['POST'])(jwt_required()(admin.reassignEmployeeProject))
admin_bp.route('/departments', methods=['GET'])(jwt_required()(admin.getDepartmentInfo))
admin_bp.route('/projects', methods=['GET'])(jwt_required()(admin.getProjectInfo))
admin_bp.route('/project_manager/<project_id>', methods=['GET'])(jwt_required()(admin.getManagerByProjectId))
admin_bp.route('/reassign_project_manager', methods=['POST'])(jwt_required()(admin.reassignProjectManager))
admin_bp.route('/positions', methods=['GET'])(jwt_required()(admin.getPositionInfo))



