from flask import Blueprint, request, jsonify
from app.services import create_user, authenticate_user

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    user = create_user(username, password, email)
    if user:
        return jsonify({'message': 'User created successfully'}), 201
    return jsonify({'message': 'User already exists'}), 400

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    token = authenticate_user(email, password)
    if token:
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401
