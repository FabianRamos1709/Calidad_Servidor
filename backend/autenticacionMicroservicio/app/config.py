import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'
    
    # Configuración de MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://root:juanangel1709@localhost/calidad_servidor'  # Cambia los valores de 'user', 'password', y 'localhost' según tu configuración
    SQLALCHEMY_TRACK_MODIFICATIONS = False
