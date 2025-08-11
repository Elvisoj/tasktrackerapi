from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import request, jsonify

def jwt_user_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'Unauthorised'}), 401
        return func(user_id=user_id, *args, **kwargs)
    return wrapper