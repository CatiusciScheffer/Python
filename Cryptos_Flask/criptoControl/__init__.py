from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
#import webview
import os

app = Flask(__name__)


#window = webview.create_window('Controle Crypto', app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # debug banco
app.config['SECRET_KEY'] = 'e264a5c0acf609e7f3ac1100562cf084'  # CHAVE SECRETA PARA SEGURANÇA
app.config['COINMARKETCAP_API_KEY'] = '122d6732-65df-475c-8f1d-d7a95ab45bc5'

db = SQLAlchemy(app)


migrate = Migrate(app, db)

def initialize_database():
    with app.app_context():
        db.create_all()


from criptoControl import routes
from criptoControl import routes_graficos

