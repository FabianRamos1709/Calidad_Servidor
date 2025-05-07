# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:CesarL26112003@localhost/agenda'  # ajusta esto
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret-key'  # reemplaza por variable de entorno en prod