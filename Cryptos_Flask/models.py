from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    wallets = db.relationship('Wallet', backref='user', lazy=True)

class Wallet(db.Model):
    __tablename__ = 'wallets'  # Corrigido aqui para 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    network = db.Column(db.String, nullable=False)
    balances = db.relationship('WalletBalance', backref='wallet', lazy=True)

class Cryptocurrency(db.Model):
    __tablename__ = 'cryptocurrencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    symbol = db.Column(db.String, unique=True, nullable=False)

class WalletBalance(db.Model):
    __tablename__ = 'wallet_balances'
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    cryptocurrency_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    wallet = db.relationship('Wallet', backref='transactions')  # Adicionando o relacionamento com Wallet
    type = db.Column(db.String, nullable=False)
    cryptocurrency_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.id'), nullable=False)
    cryptocurrency = db.relationship('Cryptocurrency', foreign_keys=[cryptocurrency_id])
    amount = db.Column(db.Float, nullable=False)
    fee_cryptocurrency_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.id'), nullable=False)
    fee_cryptocurrency = db.relationship('Cryptocurrency', foreign_keys=[fee_cryptocurrency_id])
    fee_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String, nullable=False)


class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    cryptocurrency_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.id'), nullable=False)
    cryptocurrency = db.relationship('Cryptocurrency')  # Adicione isso
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String, nullable=False)

