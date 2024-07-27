from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Wallet, Cryptocurrency, WalletBalance, Transaction, Price
from datetime import datetime
from flask_migrate import Migrate
from decimal import Decimal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # debug banco

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transacoes')
def transacoes():
    transacoes = Transaction.query.all()
    carteiras = Wallet.query.all()
    moedas = Cryptocurrency.query.all()  # Certifique-se de adicionar esta linha
    return render_template('transactions.html', transacoes=transacoes, carteiras=carteiras, moedas=moedas)

@app.route('/precos')
def precos():
    precos = Price.query.all()
    return render_template('prices.html', precos=precos)

@app.route('/carteiras')
def carteiras():
    carteiras = Wallet.query.all()
    wallet_balances = WalletBalance.query.all()
    cryptocurrencies = Cryptocurrency.query.all()

    # Criar um dicionário para armazenar os saldos por carteira e criptomoeda
    wallet_balances_dict = {}
    for balance in wallet_balances:
        if balance.wallet_id not in wallet_balances_dict:
            wallet_balances_dict[balance.wallet_id] = []
        wallet_balances_dict[balance.wallet_id].append({
            'cryptocurrency': Cryptocurrency.query.get(balance.cryptocurrency_id).name,
            'balance': balance.balance
        })

    return render_template('wallets.html', carteiras=carteiras, wallet_balances=wallet_balances_dict)


@app.route('/moedas')
def moedas():
    moedas = Cryptocurrency.query.all()
    return render_template('cryptos.html', moedas=moedas)

@app.route('/add_wallet', methods=['POST'])
def add_wallet():
    try:
        carteira_nome = request.form['name']
        carteira = Wallet(name=carteira_nome, user_id=1)  # Adicionando user_id temporariamente
        db.session.add(carteira)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao adicionar carteira: {e}")
        db.session.rollback()
    return redirect(url_for('carteiras'))

@app.route('/delete_wallet', methods=['POST'])
def delete_wallet():
    try:
        wallet_id = request.form['wallet_id']
        wallet = Wallet.query.get(wallet_id)
        if wallet:
            db.session.delete(wallet)
            db.session.commit()
    except Exception as e:
        print(f"Erro ao excluir carteira: {e}")
        db.session.rollback()
    return redirect(url_for('carteiras'))

@app.route('/add_crypto', methods=['POST'])
def add_crypto():
    try:
        cripto_name = request.form['name']
        cripto_symbol = request.form['symbol']
        cripto = Cryptocurrency(name=cripto_name, symbol=cripto_symbol)
        db.session.add(cripto)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao adicionar cripto: {e}")
        db.session.rollback()
    return redirect(url_for('moedas'))

@app.route('/add_price', methods=['POST'])
def add_price():
    try:
        crypto_id = request.form['cryptocurrency_id']
        price = float(request.form['price'])
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        crypto_price = Price(cryptocurrency_id=crypto_id, price=price, timestamp=timestamp)
        db.session.add(crypto_price)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao adicionar preço: {e}")
        db.session.rollback()
    return redirect(url_for('precos'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        wallet_id = request.form['wallet_id']
        crypto_id = request.form['cryptocurrency_id']
        amount = float(request.form['amount'])
        fee_crypto_id = request.form['fee_cryptocurrency_id']
        fee_amount = float(request.form['fee_amount'])
        transaction_type = request.form['type']

        if transaction_type == 'compra':
            realizar_compra(wallet_id, crypto_id, amount, fee_crypto_id, fee_amount)
        elif transaction_type == 'venda':
            receiving_wallet_id = request.form['receiving_wallet_id']
            receiving_crypto_id = request.form['receiving_cryptocurrency_id']
            realizar_venda(wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, receiving_wallet_id, receiving_crypto_id)
        elif transaction_type == 'transferencia':
            to_wallet_id = request.form['to_wallet_id']
            realizar_transferencia(wallet_id, to_wallet_id, crypto_id, amount, fee_crypto_id, fee_amount)

    except Exception as e:
        print(f"Erro ao adicionar transação: {e}")
        db.session.rollback()
    return redirect(url_for('transacoes'))

from sqlalchemy.exc import IntegrityError

def realizar_compra(wallet_id, crypto_id, amount, fee_crypto_id, fee_amount):
    try:
        wallet_balance = WalletBalance.query.filter_by(wallet_id=wallet_id, cryptocurrency_id=fee_crypto_id).first()

        if wallet_balance and wallet_balance.balance >= fee_amount:
            with db.session.begin():
                wallet_balance.balance -= fee_amount

                compra_balance = WalletBalance.query.filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_id).first()
                if compra_balance:
                    compra_balance.balance += amount
                else:
                    new_balance = WalletBalance(wallet_id=wallet_id, cryptocurrency_id=crypto_id, balance=amount)
                    db.session.add(new_balance)

                transacao = Transaction(wallet_id=wallet_id, type='compra', cryptocurrency_id=crypto_id, amount=amount, fee_cryptocurrency_id=fee_crypto_id, fee_amount=fee_amount, date=str(datetime.utcnow()))
                db.session.add(transacao)

            db.session.commit()
        else:
            raise ValueError("Saldo insuficiente para pagar a taxa")

    except IntegrityError:
        db.session.rollback()
        raise

def realizar_venda(wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, receiving_wallet_id, receiving_crypto_id):
    try:
        wallet_balance = WalletBalance.query.filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_id).first()
        fee_balance = WalletBalance.query.filter_by(wallet_id=wallet_id, cryptocurrency_id=fee_crypto_id).first()

        if wallet_balance and wallet_balance.balance >= amount and fee_balance and fee_balance.balance >= fee_amount:
            with db.session.begin():
                wallet_balance.balance -= amount
                fee_balance.balance -= fee_amount

                receiving_balance = WalletBalance.query.filter_by(wallet_id=receiving_wallet_id, cryptocurrency_id=receiving_crypto_id).first()
                if receiving_balance:
                    receiving_balance.balance += amount
                else:
                    new_balance = WalletBalance(wallet_id=receiving_wallet_id, cryptocurrency_id=receiving_crypto_id, balance=amount)
                    db.session.add(new_balance)

                transacao = Transaction(wallet_id=wallet_id, type='venda', cryptocurrency_id=crypto_id, amount=amount, fee_cryptocurrency_id=fee_crypto_id, fee_amount=fee_amount, date=str(datetime.utcnow()))
                db.session.add(transacao)

            db.session.commit()
        else:
            raise ValueError("Saldo insuficiente para vender ou pagar a taxa")

    except IntegrityError:
        db.session.rollback()
        raise

def realizar_transferencia(from_wallet_id, to_wallet_id, crypto_id, amount, fee_crypto_id, fee_amount):
    try:
        from_balance = WalletBalance.query.filter_by(wallet_id=from_wallet_id, cryptocurrency_id=crypto_id).first()
        fee_balance = WalletBalance.query.filter_by(wallet_id=from_wallet_id, cryptocurrency_id=fee_crypto_id).first()

        if from_balance and from_balance.balance >= amount and fee_balance and fee_balance.balance >= fee_amount:
            with db.session.begin():
                from_balance.balance -= amount
                fee_balance.balance -= fee_amount

                to_balance = WalletBalance.query.filter_by(wallet_id=to_wallet_id, cryptocurrency_id=crypto_id).first()
                if to_balance:
                    to_balance.balance += amount
                else:
                    new_balance = WalletBalance(wallet_id=to_wallet_id, cryptocurrency_id=crypto_id, balance=amount)
                    db.session.add(new_balance)

                transacao = Transaction(wallet_id=from_wallet_id, type='transferencia', cryptocurrency_id=crypto_id, amount=amount, fee_cryptocurrency_id=fee_crypto_id, fee_amount=fee_amount, date=str(datetime.utcnow()))
                db.session.add(transacao)

            db.session.commit()
        else:
            raise ValueError("Saldo insuficiente para transferir ou pagar a taxa")

    except IntegrityError:
        db.session.rollback()
        raise


@app.route('/wallets')
def show_wallets():
    # Consultar todas as carteiras e seus saldos
    wallets = Wallet.query.all()
    wallet_balances = WalletBalance.query.all()
    cryptocurrencies = Cryptocurrency.query.all()

    # Criar um dicionário para armazenar os saldos por carteira e criptomoeda
    wallet_balances_dict = {}
    for balance in wallet_balances:
        if balance.wallet_id not in wallet_balances_dict:
            wallet_balances_dict[balance.wallet_id] = []
        wallet_balances_dict[balance.wallet_id].append({
            'cryptocurrency': Cryptocurrency.query.get(balance.cryptocurrency_id).name,
            'balance': balance.balance
        })

    # Debug prints
    print("Wallets:", wallets)
    print("Wallet Balances:", wallet_balances_dict)
    
    return render_template('wallets.html', wallets=wallets, wallet_balances=wallet_balances_dict)

    

if __name__ == '__main__':
    app.run(debug=True)
