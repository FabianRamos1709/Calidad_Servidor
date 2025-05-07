from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from app.models import db
from app.routes import auth_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    JWTManager(app)

    # Registrar rutas
    app.register_blueprint(auth_routes, url_prefix='/auth')

    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
