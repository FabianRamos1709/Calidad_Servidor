from flask import Blueprint, request, jsonify
from app.services import (
    create_characteristic,
    get_all_characteristics,
    get_characteristic_by_id,
    update_characteristic,
    delete_characteristic,
    create_subcharacteristic,
    get_subcharacteristics_by_characteristic,
    get_subcharacteristic_by_id,
    update_subcharacteristic,
    delete_subcharacteristic
)


modelo_routes = Blueprint('modelo_routes', __name__)

@modelo_routes.route('/caracteristica', methods=['POST'])
def registerCharacteristic():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    weight_percentage = data.get('weight_percentage')

    software = create_characteristic(name, description, weight_percentage)
    if software:
        return jsonify({'message': 'Characteristic registered successfully'}), 201
    return jsonify({'message': 'Characteristic already exists'}), 400

@modelo_routes.route('/caracteristica', methods=['GET'])
def get_all():
    characteristics = get_all_characteristics()
    return jsonify([c.serialize() for c in characteristics]), 200

@modelo_routes.route('/caracteristica/<int:id>', methods=['GET'])
def get_one(id):
    characteristic = get_characteristic_by_id(id)
    if not characteristic:
        return jsonify({'message': 'Not found'}), 404
    return jsonify(characteristic.serialize()), 200

@modelo_routes.route('/caracteristica/<int:id>', methods=['PUT'])
def update_char(id):
    data = request.get_json()
    updated = update_characteristic(
        id,
        name=data.get('name'),
        description=data.get('description'),
        weight_percentage=data.get('weight_percentage')
    )
    if not updated:
        return jsonify({'message': 'Not found'}), 404
    return jsonify({'message': 'Updated successfully'}), 200

@modelo_routes.route('/caracteristica/<int:id>', methods=['DELETE'])
def delete_char(id):
    success = delete_characteristic(id)
    if not success:
        return jsonify({'message': 'Not found'}), 404
    return jsonify({'message': 'Deleted successfully'}), 200


@modelo_routes.route('/subcaracteristica', methods=['POST'])
def registerSubcharacteristic():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    software = create_subcharacteristic(name, description)
    if software:
        return jsonify({'message': 'Subcharacteristic registered successfully'}), 201
    return jsonify({'message': 'Subcharacteristic already exists'}), 400

@modelo_routes.route('/subcaracteristica/by_caracteristica/<int:char_id>', methods=['GET'])
def get_by_char(char_id):
    subs = get_subcharacteristics_by_characteristic(char_id)
    return jsonify([s.serialize() for s in subs]), 200

@modelo_routes.route('/subcaracteristica/<int:id>', methods=['GET'])
def get_sub(id):
    sub = get_subcharacteristic_by_id(id)
    if not sub:
        return jsonify({'message': 'Not found'}), 404
    return jsonify(sub.serialize()), 200

@modelo_routes.route('/subcaracteristica/<int:id>', methods=['PUT'])
def update_sub(id):
    data = request.get_json()
    updated = update_subcharacteristic(
        id,
        name=data.get('name'),
        description=data.get('description'),
        max_score=data.get('max_score')
    )
    if not updated:
        return jsonify({'message': 'Not found'}), 404
    return jsonify({'message': 'Updated successfully'}), 200

@modelo_routes.route('/subcaracteristica/<int:id>', methods=['DELETE'])
def delete_sub(id):
    success = delete_subcharacteristic(id)
    if not success:
        return jsonify({'message': 'Not found'}), 404
    return jsonify({'message': 'Deleted successfully'}), 200
