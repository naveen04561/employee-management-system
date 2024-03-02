from flask import Blueprint, session, request
from flask_jwt_extended import jwt_required
from controllers.AuthController import *

auth = AuthController()


auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/login', methods=['POST'])(auth.login)

auth_bp.route('/verify_phone', methods=['POST'])(jwt_required()(auth.verifyPhoneNumber))
auth_bp.route('/check_verification', methods=['POST'])(jwt_required()(auth.checkVerificationCode))



# @auth_bp.route('/login', methods=['GET'])
# def f():
#     return auth.login(request.args.get('id'), request.args.get('pass'))
