from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # debug banco
app.config['SECRET_KEY'] = 'e264a5c0acf609e7f3ac1100562cf084'  # CHAVE SECRETA PARA SEGURANÇA
app.config['COINMARKETCAP_API_KEY'] = '122d6732-65df-475c-8f1d-d7a95ab45bc5'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nome da rota para login (é importante definir isso)

@login_manager.user_loader
def load_user(user_id):
    from criptoControl.models import User  # Importa User aqui
    return User.query.get(int(user_id))

def initialize_database():
    with app.app_context():
        db.create_all()

from criptoControl import routes



