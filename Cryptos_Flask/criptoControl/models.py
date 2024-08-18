from criptoControl import db
from datetime import datetime



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
    status = db.Column(db.String(1), nullable=False, default='N' )
    balances = db.relationship('WalletBalance', backref='wallet', lazy=True)

class Cryptocurrency(db.Model):
    __tablename__ = 'cryptocurrencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    symbol = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String(1), nullable=False, default='N') 

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
    wallet = db.relationship('Wallet', foreign_keys=[wallet_id], backref='transactions')
    
    type = db.Column(db.String, nullable=False)
    
    crypto_Trans_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.id'), nullable=False)
    crypto_Trans = db.relationship('Cryptocurrency', foreign_keys=[crypto_Trans_id])
    crypto_price = db.Column(db.Float, nullable=False)
    crypto_quantity = db.Column(db.Float, nullable=False)
    transaction_total = db.Column(db.Float, nullable=False)
    
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
        
    fee_crypto_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.id'), nullable=False)
    fee_crypto = db.relationship('Cryptocurrency', foreign_keys=[fee_crypto_id])
    fee_price = db.Column(db.Float, nullable=False)
    fee_quantity = db.Column(db.Float, nullable=False)
    fee_total = db.Column(db.Float, nullable=False)

    receiving_wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=True)
    receiving_wallet = db.relationship('Wallet', foreign_keys=[receiving_wallet_id], backref='received_transactions')


class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    cryptocurrency_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.id'), nullable=False)
    cryptocurrency = db.relationship('Cryptocurrency')  # Adicione isso
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String, nullable=False)

