# routes.py
from flask import Blueprint
from controladores import autenticacion
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register', methods=['POST'])(autenticacion.register)
auth_bp.route('/login', methods=['POST'])(autenticacion.login)

auth_bp.route('/perfil', methods=['GET'])(jwt_required()(autenticacion.perfil))