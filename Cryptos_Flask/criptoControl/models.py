from criptoControl import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    user_wallets = db.relationship('Wallet', backref='user', lazy=True)

class Wallet(db.Model):
    __tablename__ = 'wallets'  # Corrigido aqui para 'wallets'
    wallet_id = db.Column(db.Integer, primary_key=True)
    wallet_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    wallet_name = db.Column(db.String, nullable=False)
    wallet_network = db.Column(db.String, nullable=False)
    wallet_status = db.Column(db.String(1), nullable=False, default='N' )
    #balances = db.relationship('WalletBalance', backref='payment_wallet', lazy=True)

class Cryptocurrency(db.Model):
    __tablename__ = 'cryptocurrencies'
    crypto_id = db.Column(db.Integer, primary_key=True)
    crypto_name = db.Column(db.String, unique=True, nullable=False)
    crypto_symbol = db.Column(db.String, unique=True, nullable=False)
    crypto_status = db.Column(db.String(1), nullable=False, default='N') 

class WalletBalance(db.Model):
    __tablename__ = 'wallet_balances'
    balance_id = db.Column(db.Integer, primary_key=True)
    balance_wallet_id = db.Column(db.Integer, nullable=False)
    balance_crypto_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    # Dados da transação
    transactions_id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False, default=datetime.now)
    
    # Carteira de pagamento
    payment_wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.wallet_id'), nullable=True)
    payment_wallet = db.relationship('Wallet', foreign_keys=[payment_wallet_id], backref='transactions')
    
    # Carteira de recebimento
    receiving_wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.wallet_id'), nullable=True)
    receiving_wallet = db.relationship('Wallet', foreign_keys=[receiving_wallet_id], backref='received_transactions')

    # Cripto pagamento
    crypto_payment_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=True)
    crypto_payment = db.relationship('Cryptocurrency', foreign_keys=[crypto_payment_id])
    crypto_payment_price = db.Column(db.Float, nullable=True)
    crypto_payment_quantity = db.Column(db.Float, nullable=True)
    total_paid = db.Column(db.Float, nullable=True)
    
    # Cripto recebimento
    crypto_receive_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=True)
    crypto_receive = db.relationship('Cryptocurrency', foreign_keys=[crypto_receive_id])  # Corrigido para usar crypto_receive_id
    crypto_receive_price = db.Column(db.Float, nullable=True)
    crypto_receive_quantity = db.Column(db.Float, nullable=True)
    total_received = db.Column(db.Float, nullable=True)

    # Cripto taxa    
    crypto_fee_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=True)
    crypto_fee = db.relationship('Cryptocurrency', foreign_keys=[crypto_fee_id])
    crypto_fee_price = db.Column(db.Float, nullable=True)
    crypto_fee_quantity = db.Column(db.Float, nullable=True)
    total_fee = db.Column(db.Float, nullable=True)
   


class Price(db.Model):
    __tablename__ = 'prices'
    price_id = db.Column(db.Integer, primary_key=True)
    price_crypto_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=False)
    price_cryptocurrency = db.relationship('Cryptocurrency')  
    price = db.Column(db.Float, nullable=False)
    price_consult_datetime = db.Column(db.String, nullable=False)#não mudar tipo!


