# controllers/auth_controller.py
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from modelos.usuarios import db, Usuario

bcrypt = Bcrypt()

# Registro
def register():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data['contrasena']).decode('utf-8')
    nuevo_usuario = User(nombre=data['nombre'], correo=data['correo'], contrasena=hashed_pw)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuario registrado correctamente"}), 201

# Login
def login():
    data = request.get_json()
    usuario = User.query.filter_by(correo=data['correo']).first()
    if usuario and bcrypt.check_password_hash(usuario.contrasena, data['contrasena']):
        token = create_access_token(identity={"id": usuario.id, "rol": usuario.rol})
        return jsonify({"access_token": token})
    return jsonify({"error": "Credenciales inválidas"}), 401

# Ruta protegida
@jwt_required()
def perfil():
    user_info = get_jwt_identity()
    return jsonify({"mensaje": f"Bienvenido usuario con rol {user_info['rol']}"})