from flask import Blueprint, request, jsonify
from app.utils.auth import create_user, find_user_by_email
from app.extensions import jwt
from flask_jwt_extended import create_access_token
from flasgger.utils import swag_from


login_error = {'error': 'Invalid Credentials'}
field_error = {'error': 'All fields are required'}
already_exit_user_error = {'error': 'User already exists'}


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route("/register", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Register a new user',
    'description': 'Creates a new user account.',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'User created successfully'},
        400: {'description': 'User already exists or invalid data'}
    }
})
def register():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('firstname')
    username = data.get('firstname')
    email = data.get('email')
    password = data.get('password')

    if not all([firstname, lastname, username, email, password]):
        return jsonify(field_error), 400
    
    if find_user_by_email(email):
        return jsonify(already_exit_user_error), 400
    
    user = create_user(firstname, lastname, username, email, password)
    return jsonify({'message': 'User registerd successfully', 'username': user.username}), 201


@auth_bp.route("/login", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'summary': 'User login',
    'description': 'Authenticates user and returns JWT token.',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Login successful'},
        401: {'description': 'Invalid credentials'}
    }
})

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = find_user_by_email(email)

    if not user or not user.check_password(password):
        return jsonify(login_error), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token, 'username': user.username}), 200