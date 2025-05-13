from flask import Blueprint, request, jsonify
from app.services import create_software_with_participants

software_routes = Blueprint('software_routes', __name__)

@software_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    city = data.get('city')
    general_objective = data.get('general_objective')
    description = data.get('description')
    version = data.get('version'),
    user_id = data.get('user_id'),
    participants = data.get('participants', [])  # lista de diccionarios

    result = create_software_with_participants(name, city, general_objective, description, version, participants, user_id)
    if result['success']:
        return jsonify({'message': 'Software registrado exitosamente'}), 201
    return jsonify({'message': result['message']}), 400
