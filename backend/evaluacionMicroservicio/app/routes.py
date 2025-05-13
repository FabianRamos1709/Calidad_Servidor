from flask import Blueprint, request, jsonify
from app.services import create_evaluation

evaluation_routes = Blueprint('evaluation_routes', __name__)

@evaluation_routes.route('/evaluar', methods=['POST'])
def create_evaluation_route():
    data = request.get_json()
    evaluation, error = create_evaluation(data)
    if error:
        return jsonify({'message': 'Error guardando la evaluación', 'error': error}), 400

    return jsonify({'message': 'Evaluación guardada exitosamente', 'evaluation_id': evaluation.id}), 201
