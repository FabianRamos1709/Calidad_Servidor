from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from flask_jwt_extended import create_access_token

def create_user(username, password, email):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return None

    password_hash = generate_password_hash(password)
    new_user = User(username=username, password_hash=password_hash, email=email)

    db.session.add(new_user)
    db.session.commit()
    return new_user

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        token = create_access_token(identity=user.id)
        return token
    return None
