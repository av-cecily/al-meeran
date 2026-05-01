from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/login', methods=['POST'])(AuthController.login)
auth_bp.route('/forgot-password', methods=['POST'])(AuthController.forgot_password)
auth_bp.route('/reset-password', methods=['POST'])(AuthController.reset_password)
