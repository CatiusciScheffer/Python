from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from models import db, User, Wallet, Cryptocurrency, WalletBalance, Transaction, Price
from api import get_crypto_price
from api import get_crypto_price
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # debug banco

db.init_app(app)
migrate = Migrate(app, db)

# Substitua com sua chave de API da CoinMarketCap
COINMARKETCAP_API_KEY = '122d6732-65df-475c-8f1d-d7a95ab45bc5'

def create_session():
    return sessionmaker(bind=db.engine)()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transacoes')
def transacoes():
    with app.app_context():
        session = create_session()
        transacoes = session.query(Transaction).all()
        carteiras = session.query(Wallet).all()
        moedas = session.query(Cryptocurrency).all()
        total_values = [{'id': t.id, 'total': t.amount * t.amount_paid} for t in transacoes]
    return render_template('transactions.html', transacoes=transacoes, carteiras=carteiras, moedas=moedas, total_values=total_values)

@app.route('/precos')
def precos():
    with app.app_context():
        session = create_session()
        precos = session.query(Price).all()
    return render_template('prices.html', precos=precos)

@app.route('/carteiras')
def carteiras():
    with app.app_context():
        session = create_session()
        carteiras = session.query(Wallet).all()
        wallet_balances = session.query(WalletBalance).all()
        cryptocurrencies = session.query(Cryptocurrency).all()

        wallet_balances_dict = {}
        for balance in wallet_balances:
            if balance.wallet_id not in wallet_balances_dict:
                wallet_balances_dict[balance.wallet_id] = []
            wallet_balances_dict[balance.wallet_id].append({
                'cryptocurrency': session.query(Cryptocurrency).get(balance.cryptocurrency_id).name,
                'balance': balance.balance
            })

    return render_template('wallets.html', carteiras=carteiras, wallet_balances=wallet_balances_dict)

@app.route('/moedas')
def moedas():
    with app.app_context():
        session = create_session()
        moedas = session.query(Cryptocurrency).all()
    return render_template('cryptos.html', moedas=moedas)

@app.route('/add_wallet', methods=['POST'])
def add_wallet():
    try:
        carteira_nome = request.form['name']
        network = request.form['network']
        with app.app_context():
            session = create_session()
            carteira = Wallet(name=carteira_nome, network=network, user_id=1)  # Adicionando user_id temporariamente
            session.add(carteira)
            session.commit()
    except Exception as e:
        print(f"Erro ao adicionar carteira: {e}")
        session.rollback()
    return redirect(url_for('carteiras'))

@app.route('/delete_wallet', methods=['POST'])
def delete_wallet():
    try:
        wallet_id = request.form['wallet_id']
        with app.app_context():
            session = create_session()
            wallet = session.query(Wallet).get(wallet_id)
            if wallet:
                session.delete(wallet)
                session.commit()
    except Exception as e:
        print(f"Erro ao excluir carteira: {e}")
        session.rollback()
    return redirect(url_for('carteiras'))

@app.route('/add_crypto', methods=['POST'])
def add_crypto():
    try:
        cripto_name = request.form['name']
        cripto_symbol = request.form['symbol']
        with app.app_context():
            session = create_session()
            cripto = Cryptocurrency(name=cripto_name, symbol=cripto_symbol)
            session.add(cripto)
            session.commit()
    except Exception as e:
        print(f"Erro ao adicionar cripto: {e}")
        session.rollback()
    return redirect(url_for('moedas'))

@app.route('/add_price', methods=['POST'])
def add_price():
    try:
        crypto_id = request.form['cryptocurrency_id']
        price = float(request.form['price'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with app.app_context():
            session = create_session()
            crypto_price = Price(cryptocurrency_id=crypto_id, price=price, timestamp=timestamp)
            session.add(crypto_price)
            session.commit()
    except Exception as e:
        print(f"Erro ao adicionar preço: {e}")
        session.rollback()
    return redirect(url_for('precos'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        wallet_id = request.form['wallet_id']
        crypto_id = request.form['cryptocurrency_id']
        amount = float(request.form['amount'])
        fee_crypto_id = request.form['fee_cryptocurrency_id']
        fee_amount = float(request.form['fee_amount'])
        transaction_type = request.form['transaction_type']
        amount_paid = float(request.form['amount_paid'])

        with app.app_context():
            session = create_session()
            if transaction_type == 'compra':
                realizar_compra(session, wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, amount_paid)
            elif transaction_type == 'venda':
                realizar_venda(session, wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, amount_paid)
            elif transaction_type == 'transferencia':
                to_wallet_id = request.form['receiving_wallet_id']
                realizar_transferencia(session, wallet_id, to_wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, amount_paid)

    except Exception as e:
        print(f"Erro ao adicionar transação: {e}")
        session.rollback()
    return redirect(url_for('transacoes'))

@app.route('/update_prices', methods=['POST'])
def update_prices():
    try:
        with app.app_context():
            session = create_session()
            cryptocurrencies = session.query(Cryptocurrency).all()
            for crypto in cryptocurrencies:
                price = get_crypto_price(COINMARKETCAP_API_KEY, crypto.symbol)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                crypto_price = Price(cryptocurrency_id=crypto.id, price=price, timestamp=timestamp)
                session.add(crypto_price)
            session.commit()
    except Exception as e:
        print(f"Erro ao atualizar preços: {e}")
        session.rollback()
    return redirect(url_for('index'))

def realizar_compra(session, wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, amount_paid):
    new_transaction = Transaction(
        wallet_id=wallet_id, 
        type='compra', 
        cryptocurrency_id=crypto_id, 
        amount=amount, 
        amount_paid=amount_paid,
        fee_cryptocurrency_id=fee_crypto_id, 
        fee_amount=fee_amount, 
        date=datetime.now()
    )
    session.add(new_transaction)
    balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_id).first()
    if balance:
        balance.balance += amount
    else:
        new_balance = WalletBalance(wallet_id=wallet_id, cryptocurrency_id=crypto_id, balance=amount)
        session.add(new_balance)
    session.commit()

def realizar_venda(session, wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, amount_paid):
    new_transaction = Transaction(
        wallet_id=wallet_id, 
        type='venda', 
        cryptocurrency_id=crypto_id, 
        amount=amount, 
        amount_paid=amount_paid,
        fee_cryptocurrency_id=fee_crypto_id, 
        fee_amount=fee_amount, 
        date=datetime.now()
    )
    session.add(new_transaction)
    balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_id).first()
    if balance and balance.balance >= amount:
        balance.balance -= amount
        session.commit()
    else:
        raise ValueError("Saldo insuficiente para a venda.")

def realizar_transferencia(session, from_wallet_id, to_wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, amount_paid):
    new_transaction = Transaction(
        wallet_id=from_wallet_id, 
        type='transferencia', 
        cryptocurrency_id=crypto_id, 
        amount=amount, 
        amount_paid=amount_paid,
        fee_cryptocurrency_id=fee_crypto_id, 
        fee_amount=fee_amount, 
        date=datetime.now(), 
        receiving_wallet_id=to_wallet_id
    )
    session.add(new_transaction)

    from_balance = session.query(WalletBalance).filter_by(wallet_id=from_wallet_id, cryptocurrency_id=crypto_id).first()
    if from_balance and from_balance.balance >= amount:
        from_balance.balance -= amount
    else:
        raise ValueError("Saldo insuficiente para a transferência.")

    to_balance = session.query(WalletBalance).filter_by(wallet_id=to_wallet_id, cryptocurrency_id=crypto_id).first()
    if to_balance:
        to_balance.balance += amount
    else:
        new_balance = WalletBalance(wallet_id=to_wallet_id, cryptocurrency_id=crypto_id, balance=amount)
        session.add(new_balance)

    session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

