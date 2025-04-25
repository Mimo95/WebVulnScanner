import os
import logging
from datetime import timedelta


# Définir le chemin de base du projet
basedir = os.path.abspath(os.path.dirname(__file__))

# Création des dossiers si besoin
os.makedirs(os.path.join(basedir, 'logs'), exist_ok=True)
os.makedirs(os.path.join(basedir, 'database'), exist_ok=True)

# Configuration du logging
logging.basicConfig(
    filename=os.path.join(basedir, 'logs', 'app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Classe de configuration Flask
class Config:
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret-key'

    JWT_SECRET_KEY = "votre_jwt_secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=30) # 15 min, 30 sec pendant les tests
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
