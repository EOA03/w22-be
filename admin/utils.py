from flask import request, g
from functools import wraps
from auth.utils import decode_jwt

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return {"error": "Invalid token format"}, 401

        token = auth_header.split(' ')[1]

        try:
            payload = decode_jwt(token)
        except Exception as e:
            print(f"Error decoding token: {e}")
            return {"error": "Token is invalid"}, 401

        if not payload or "role" not in payload:
            return {"error": "Token is invalid"}, 401
        
        if payload['role'] != 'admin':
            return {"error": "Unauthorized, Admin role required"}, 403
        
        g.current_user = payload
        return func(*args, **kwargs)

    return wrapper