from flask import Blueprint, request, jsonify
from app.services import create_software, create_participant

software_routes = Blueprint('software_routes', __name__)

@software_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    city = data.get('city')
    general_objective = data.get('general_objective')
    description = data.get('description')
    version = data.get('version')

    software = create_software(name, city, general_objective, description, version)
    if software:
        return jsonify({'message': 'Software registered successfully'}), 201
    return jsonify({'message': 'Software already exists'}), 400

@software_routes.route('/register/participants', methods=['POST'])
def registerParticipant():
    data = request.get_json()
    name = data.get('name')
    role = data.get('role')

    participant = create_participant(name, role)
    if participant:
        return jsonify({'message': 'Participant registered successfully'}), 201
    return jsonify({'message': 'Participant already exists'}), 400
