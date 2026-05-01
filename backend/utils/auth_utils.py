import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv('JWT_SECRET', 'meeran_secret_2026')

def generate_token(username):
    payload = {
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Unauthorized'}), 401
        try:
            if "Bearer " in token:
                token = token.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return jsonify({'error': 'Invalid Token'}), 401
        return f(*args, **kwargs)
    return decorated
