from flask import Blueprint, request, jsonify
from app.models import db
from app.services import (
    get_characteristic_with_subs,
    create_characteristic_with_subs,
    get_all_characteristics,
    update_characteristic_with_subs,
    delete_characteristic,
    delete_subcharacteristic
)


modelo_routes = Blueprint('modelo_routes', __name__)

@modelo_routes.route('/caracteristica', methods=['POST'])
def create_characteristic():
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description')
    weight_percentage = data.get('weight_percentage')
    subcharacteristics = data.get('subcharacteristics', [])

    if not name or not isinstance(subcharacteristics, list):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        new_char = create_characteristic_with_subs(name, description, weight_percentage, subcharacteristics)
        return jsonify({
            "message": "Característica creada exitosamente",
            "characteristic_id": new_char.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@modelo_routes.route('/caracteristica', methods=['GET'])
def get_all():
    characteristics = get_all_characteristics()
    return jsonify(characteristics), 200

@modelo_routes.route('/caracteristica/<int:char_id>', methods=['GET'])
def get_characteristic_with_subs_route(char_id):
    result = get_characteristic_with_subs(char_id)
    if not result:
        return jsonify({'message': 'Characteristic not found'}), 404
    return jsonify(result), 200


@modelo_routes.route('/caracteristica/<int:char_id>', methods=['PUT'])
def updateCharacteristicWithSubs(char_id):
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    weight_percentage = data.get('weight_percentage')
    subcharacteristics = data.get('subcharacteristics', [])

    result = update_characteristic_with_subs(
        char_id,
        name,
        description,
        weight_percentage,
        subcharacteristics
    )

    if result:
        return jsonify({'message': 'Characteristic and subcharacteristics updated successfully'}), 200
    else:
        return jsonify({'message': 'Characteristic not found'}), 404

@modelo_routes.route('/caracteristica/<int:id>', methods=['DELETE'])
def delete_char(id):
    success = delete_characteristic(id)
    if not success:
        return jsonify({'message': 'Not found'}), 404
    return jsonify({'message': 'Deleted successfully'}), 200

@modelo_routes.route('/subcaracteristica/<int:id>', methods=['DELETE'])
def delete_sub(id):
    success = delete_subcharacteristic(id)
    if not success:
        return jsonify({'message': 'Not found'}), 404
    return jsonify({'message': 'Deleted successfully'}), 200
