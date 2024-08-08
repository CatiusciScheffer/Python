from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from models import db, User, Wallet, Cryptocurrency, WalletBalance, Transaction, Price
from forms import TransacaoForm
from api import get_crypto_price
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # debug banco
app.config['SECRET_KEY'] = 'e264a5c0acf609e7f3ac1100562cf084' #CHAVE SECRETA PARA SEGURANÇA

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
    formTransacoes = TransacaoForm()
    with app.app_context():
        session = create_session()
        transacoes = session.query(Transaction).all()
        carteiras = session.query(Wallet).all()
        moedas = session.query(Cryptocurrency).all()
        total_values = [{'id': t.id, 'total': t.amount * t.amount_paid} for t in transacoes]
    return render_template('transactions.html', transacoes=transacoes, carteiras=carteiras, moedas=moedas, total_values=total_values, formTransacoes=formTransacoes)

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
        receiving_wallet_id = request.form['receiving_wallet_id']

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
    # Lógica para realizar uma compra
    wallet = session.query(Wallet).get(wallet_id)
    crypto = session.query(Cryptocurrency).get(crypto_id)
    fee_crypto = session.query(Cryptocurrency).get(fee_crypto_id)

    # Atualizar o saldo da carteira
    wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_id).first()
    if wallet_balance:
        wallet_balance.balance += amount
    else:
        wallet_balance = WalletBalance(wallet_id=wallet_id, cryptocurrency_id=crypto_id, balance=amount)
        session.add(wallet_balance)
    
    # Registrar a transação
    transaction = Transaction(
        wallet_id=wallet_id,
        cryptocurrency_id=crypto_id,
        amount=amount,
        fee_cryptocurrency_id=fee_crypto_id,
        fee_amount=fee_amount,
        date=datetime.now(),
        amount_paid=amount_paid,
        type='compra'
    )
    session.add(transaction)

    # Deduzir a taxa
    wallet_balance_fee = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=fee_crypto_id).first()
    if wallet_balance_fee:
        wallet_balance_fee.balance -= fee_amount
    else:
        wallet_balance_fee = WalletBalance(wallet_id=wallet_id, cryptocurrency_id=fee_crypto_id, balance=-fee_amount)
        session.add(wallet_balance_fee)
    
    session.commit()

def realizar_venda(session, wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, amount_paid):
    print("Iniciando a função realizar_venda")
    try:
        # Lógica para realizar uma venda
        wallet = session.query(Wallet).get(wallet_id)
        crypto = session.query(Cryptocurrency).get(crypto_id)
        fee_crypto = session.query(Cryptocurrency).get(fee_crypto_id)
        
        if not wallet:
            print(f"Carteira {wallet_id} não encontrada.")
            return
        if not crypto:
            print(f"Criptomoeda {crypto_id} não encontrada.")
            return
        if not fee_crypto:
            print(f"Criptomoeda da taxa {fee_crypto_id} não encontrada.")
            return

        # Atualizar o saldo da carteira
        wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_id).first()
        if wallet_balance:
            wallet_balance.balance -= amount
            if wallet_balance.balance < 0:
                print("Saldo insuficiente para realizar a venda.")
                return
            else:
                print(f"Saldo não encontrado para a carteira {wallet_id} e criptomoeda {crypto_id}.")
                return
        else:
            wallet_balance = WalletBalance(wallet_id=wallet_id, cryptocurrency_id=crypto_id, balance=amount)
            session.add(wallet_balance)
             
        # Registrar a transação
        transaction = Transaction(
            wallet_id=wallet_id,
            cryptocurrency_id=crypto_id,
            amount=amount,
            fee_cryptocurrency_id=fee_crypto_id,
            fee_amount=fee_amount,
            date=datetime.now(),
            amount_paid=amount_paid,
            type='venda'
        )
        session.add(transaction)

        # Deduzir a taxa
        wallet_balance_fee = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=fee_crypto_id).first()
        if wallet_balance_fee:
            wallet_balance_fee.balance -= fee_amount
            if wallet_balance_fee.balance < 0:
                print("Saldo insuficiente para deduzir a taxa.")
                return
        else:
            wallet_balance_fee = WalletBalance(wallet_id=wallet_id, cryptocurrency_id=fee_crypto_id, balance=-fee_amount)
            session.add(wallet_balance_fee)
        
        session.commit()
        print("Venda realizada com sucesso.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao realizar venda: {e}")

def realizar_transferencia(session, from_wallet_id, to_wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, amount_paid):
    # Lógica para realizar uma transferência
    from_wallet_balance = session.query(WalletBalance).filter_by(wallet_id=from_wallet_id, cryptocurrency_id=crypto_id).first()
    if from_wallet_balance:
        from_wallet_balance.balance -= amount
    else:
        from_wallet_balance = WalletBalance(wallet_id=from_wallet_id, cryptocurrency_id=crypto_id, balance=-amount)
        session.add(from_wallet_balance)
    
    to_wallet_balance = session.query(WalletBalance).filter_by(wallet_id=to_wallet_id, cryptocurrency_id=crypto_id).first()
    if to_wallet_balance:
        to_wallet_balance.balance += amount
    else:
        to_wallet_balance = WalletBalance(wallet_id=to_wallet_id, cryptocurrency_id=crypto_id, balance=amount)
        session.add(to_wallet_balance)

    # Registrar a transação
    transaction = Transaction(
        wallet_id=from_wallet_id,
        cryptocurrency_id=crypto_id,
        amount=amount,
        fee_cryptocurrency_id=fee_crypto_id,
        fee_amount=fee_amount,
        receiving_wallet_id=to_wallet_id,
        date=datetime.now(),
        amount_paid=amount_paid,
        type='transferencia'
    )
    session.add(transaction)

    # Deduzir a taxa
    fee_wallet_balance = session.query(WalletBalance).filter_by(wallet_id=from_wallet_id, cryptocurrency_id=fee_crypto_id).first()
    if fee_wallet_balance:
        fee_wallet_balance.balance -= fee_amount
    else:
        fee_wallet_balance = WalletBalance(wallet_id=from_wallet_id, cryptocurrency_id=fee_crypto_id, balance=-fee_amount)
        session.add(fee_wallet_balance)

    session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

