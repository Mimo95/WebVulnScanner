from models import User
from database import db
from werkzeug.security import generate_password_hash

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

def create_user(username, email, password):
    if User.query.filter_by(username=username).first() is not None:
        return "Nom d'utilisateur déjà existant"
    if User.query.filter_by(email=email).first() is not None:
        return "Adresse e-mail déjà existante"
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return None