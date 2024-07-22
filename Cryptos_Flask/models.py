from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'  # Define o caminho para o banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define as classes do SQLAlchemy para cada tabela
class Carteira(db.Model):
    id_carteira = db.Column(db.Integer, primary_key=True)
    carteira_nome = db.Column(db.String(80), nullable=False)

class Cripto(db.Model):
    id_cripto = db.Column(db.Integer, primary_key=True)
    cripto_name = db.Column(db.String(80), nullable=False)
    cripto_apelido = db.Column(db.String(80), nullable=False)

class CryptoPrice(db.Model):
    id_cripto_price = db.Column(db.Integer, primary_key=True)
    cripto_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class Transacao(db.Model):
    id_trans = db.Column(db.Integer, primary_key=True)
    cripto_name = db.Column(db.String(80), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    taxa = db.Column(db.Float, nullable=True)
    date = db.Column(db.Date, nullable=False)
    destino = db.Column(db.String(80), nullable=True)
    origem = db.Column(db.String(80), nullable=False)
    tipo_transacao = db.Column(db.String(80), nullable=False)

# Cria as tabelas no banco de dados se elas não existirem
with app.app_context():
    db.create_all()
