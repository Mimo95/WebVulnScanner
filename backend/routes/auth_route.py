from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from models import User, TokenBlocklist
from services.auth_service import authenticate_user, create_user
from schemas import UserSchema
from marshmallow import ValidationError
from database import db

auth_bp = Blueprint("auth", __name__)
user_schema = UserSchema()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Nom d\'utilisateur et mot de passe requis'}), 400

    user = authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({'message': 'Connexion réussie', 'access_token': access_token, 'refresh_token': refresh_token}), 200
    else:
        return jsonify({'message': 'Identifiants invalides'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        validated_data = user_schema.load(data)
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = data.get('password')

        if not password:
            return jsonify({'message': 'Mot de passe requis'}), 400

        registration_result = create_user(username, email, password)

        if registration_result is None:
            return jsonify({'message': 'Utilisateur enregistré avec succès'}), 201
        elif registration_result == "Nom d'utilisateur déjà existant":
            return jsonify({'message': registration_result}), 409
        elif registration_result == "Adresse e-mail déjà existante":
            return jsonify({'message': registration_result}), 409
        else:
            return jsonify({'message': 'Erreur lors de l\'enregistrement'}), 500
    except ValidationError as err:
        return jsonify(err.messages), 400
        
@auth_bp.get("/whoami")
@jwt_required()
def whoami():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if user:
        result = user_schema.dump(user)
        return jsonify({"message": "Informations de l'utilisateur courant", "user_details": result}), 200
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token})

@auth_bp.route('/logout' , methods=['POST'])
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()
    jti = jwt['jti']
    token_type = jwt['type']
    
    blocked_token = TokenBlocklist(jti=jti)
    db.session.add(blocked_token)
    db.session.commit()
    
    return jsonify({"message": f"{token_type} token révoqué avec succès"}), 200
