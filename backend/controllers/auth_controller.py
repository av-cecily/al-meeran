from flask import request, jsonify
from models.admin import Admin
from utils.auth_utils import generate_token
import os

class AuthController:
    @staticmethod
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user = Admin.get_by_username(username)
        if user and Admin.verify_password(user['password'], password):
            token = generate_token(username)
            return jsonify({'token': token}), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401

    @staticmethod
    def forgot_password():
        # Placeholder for forgot password logic
        # In a real app, this would send an email with a reset code
        data = request.json
        username = data.get('username')
        user = Admin.get_by_username(username)
        if user:
            # Here you would generate a code and send it via email
            return jsonify({'message': 'If the user exists, a reset code has been sent'}), 200
        return jsonify({'message': 'If the user exists, a reset code has been sent'}), 200

    @staticmethod
    def reset_password():
        # Placeholder for reset password logic
        data = request.json
        # logic to verify code and update password
        return jsonify({'message': 'Password reset successful'}), 200
