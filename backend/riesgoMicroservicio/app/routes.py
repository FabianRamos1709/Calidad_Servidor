from flask import Blueprint, request, jsonify
from app.services import register_software_risk

riesgo_routes = Blueprint('risk', __name__)

@riesgo_routes.route('/registrar', methods=['POST'])
def register_risk():
    data = request.get_json()
    result, status = register_software_risk(data)
    return jsonify(result), status
