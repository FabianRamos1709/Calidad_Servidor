# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config
from rutas import auth_bp

# Inicialización
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Registrar blueprint
app.register_blueprint(auth_bp)

# Crear tablas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
