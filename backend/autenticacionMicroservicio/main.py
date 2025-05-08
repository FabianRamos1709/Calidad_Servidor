import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from backend.config import Config
from app.models import db
from app.routes import auth_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)  # ⬅️ Esta línea es nueva

    app.register_blueprint(auth_routes, url_prefix='/auth')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
