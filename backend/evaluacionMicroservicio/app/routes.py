from flask import Blueprint, request, jsonify
from app.services import create_evaluation, get_evaluation_details_by_software_id, get_evaluated_softwares_by_user, get_characteristic_summary_by_software

evaluation_routes = Blueprint('evaluation_routes', __name__)

@evaluation_routes.route('/evaluar', methods=['POST'])
def create_evaluation_route():
    data = request.get_json()
    evaluation, error = create_evaluation(data)
    if error:
        return jsonify({'message': 'Error guardando la evaluación', 'error': error}), 400

    return jsonify({'message': 'Evaluación guardada exitosamente', 'evaluation_id': evaluation.id}), 201

@evaluation_routes.route('/detalle/<int:software_id>', methods=['GET'])
def get_evaluation_details(software_id):
    try:
        data = get_evaluation_details_by_software_id(software_id)
        if not data:
            return jsonify({'success': False, 'message': 'No se encontraron evaluaciones para este software'}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@evaluation_routes.route('/software-evaluados/<int:user_id>', methods=['GET'])
def get_evaluated_softwares(user_id):
    try:
        data = get_evaluated_softwares_by_user(user_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@evaluation_routes.route('/resultados/<int:software_id>//<int:evaluation_id>', methods=['GET'])
def get_software_characteristic_summary(software_id, evaluation_id):
    try:
        data = get_characteristic_summary_by_software(software_id, evaluation_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    