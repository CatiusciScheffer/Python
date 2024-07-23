from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

class Transacao(db.Model):
    id_trans = db.Column(db.Integer, primary_key=True)
    cripto_name = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Numeric(precision=20, scale=10), nullable=False)
    preco = db.Column(db.Numeric(precision=20, scale=10), nullable=False)
    taxa = db.Column(db.Numeric(precision=20, scale=10))
    date = db.Column(db.Date, nullable=False)
    # Definindo as chaves estrangeiras corretamente
    destino_id = db.Column(db.Integer, db.ForeignKey('carteira.id_carteira'), nullable=False)
    origem_id = db.Column(db.Integer, db.ForeignKey('carteira.id_carteira'), nullable=False)
    tipo_transacao = db.Column(db.String(50), nullable=False)

    # Relacionamento com a tabela Carteira
    destino = db.relationship('Carteira', foreign_keys=[destino_id], backref='transacoes_destino')
    origem = db.relationship('Carteira', foreign_keys=[origem_id], backref='transacoes_origem')

class Carteira(db.Model):
    id_carteira = db.Column(db.Integer, primary_key=True)
    carteira_nome = db.Column(db.String(50), nullable=False)
    saldos = db.relationship('CarteiraSaldo', back_populates='carteira', lazy=True)

class Cripto(db.Model):
    id_cripto = db.Column(db.Integer, primary_key=True)
    cripto_name = db.Column(db.String(80), nullable=False)
    cripto_apelido = db.Column(db.String(80), nullable=False)
    saldos = db.relationship('CarteiraSaldo', back_populates='cripto', lazy=True)

class CarteiraSaldo(db.Model):
    id_saldo = db.Column(db.Integer, primary_key=True)
    carteira_id = db.Column(db.Integer, db.ForeignKey('carteira.id_carteira'), nullable=False)
    cripto_id = db.Column(db.Integer, db.ForeignKey('cripto.id_cripto'), nullable=False)
    saldo = db.Column(db.Float, nullable=False, default=0.0)

    carteira = db.relationship('Carteira', back_populates='saldos')
    cripto = db.relationship('Cripto', back_populates='saldos')

class CryptoPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(precision=20, scale=10), nullable=False)