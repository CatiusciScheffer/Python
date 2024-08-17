from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # debug banco
app.config['SECRET_KEY'] = 'e264a5c0acf609e7f3ac1100562cf084' #CHAVE SECRETA PARA SEGURANÇA
app.config['COINMARKETCAP_API_KEY'] = '122d6732-65df-475c-8f1d-d7a95ab45bc5'

db = SQLAlchemy(app)

migrate = Migrate(app, db)




from criptoControl import routes
