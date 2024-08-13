from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from models import db, User, Wallet, Cryptocurrency, WalletBalance, Transaction, Price
from forms import TransacaoForm, AddWalletForm, AddCryptoForm
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


#----------------------  INICIO ROTAS -------------------------
#***** ROTA INDEX *****
@app.route('/')
def index():
    formTransacoes = TransacaoForm()
    formAddCarteiras = AddWalletForm()
    formAddMoedas = AddCryptoForm()
    session = create_session()

    #busca as informações no banco
    transacoes = session.query(Transaction).all()
    carteiras = session.query(Wallet).filter(Wallet.status=='N').all()
    moedas = session.query(Cryptocurrency).filter(Cryptocurrency.status=='N').all()

    #Popular as informações do banco no html
    formTransacoes.moedaTransacao.choices = [(moeda.id, f"{moeda.name} ({moeda.symbol})") for moeda in moedas]
    formTransacoes.moedaTaxa.choices = [(moeda.id, f"{moeda.name} ({moeda.symbol})") for moeda in moedas]
    formTransacoes.carteriaSaidaTransacao.choices = [(carteira.id, carteira.name) for carteira in carteiras]
    formTransacoes.carteriaRecebimentoTransacao.choices = [(carteira.id, carteira.name) for carteira in carteiras]
    
    return render_template('index.html', transacoes=transacoes, carteiras=carteiras, moedas=moedas, formTransacoes=formTransacoes, formAddCarteiras=formAddCarteiras, formAddMoedas=formAddMoedas)


#***** ROTA TRANSAÇÕES *****
@app.route('/transacoes')
def transacoes():
    
    with app.app_context():
        session = create_session()
        
        total_values = [{'id': t.id, 'total': t.amount * t.amount_paid} for t in transacoes]        

    return render_template('transactions.html', total_values=total_values)


#***** ROTA PREÇOS *****
@app.route('/precos')
def precos():
    with app.app_context():
        session = create_session()
        
        # Subconsulta para obter o preço mais recente de cada criptomoeda
        subquery = (
            session.query(Price.cryptocurrency_id, func.max(Price.timestamp).label('latest_timestamp'))
            .group_by(Price.cryptocurrency_id)
            .subquery()
        )
        
        # Consulta principal para obter os preços mais recentes
        precos = (
            session.query(Price)
            .join(subquery, (Price.cryptocurrency_id == subquery.c.cryptocurrency_id) &
                                (Price.timestamp == subquery.c.latest_timestamp))
            .join(Cryptocurrency, Price.cryptocurrency_id == Cryptocurrency.id)
            .filter(Cryptocurrency.status == 'N')
            .all()
        )
    
    return render_template('prices.html', precos=precos)



#***** ROTA CARTEIRAS *****
@app.route('/carteiras')
def carteiras():
    with app.app_context():
        carteiras = Wallet.query.filter(Wallet.status != 'S').order_by(Wallet.name).all()
    return render_template('wallets.html', carteiras=carteiras)


#***** ROTA MOEDAS *****
@app.route('/moedas')
def moedas():
    with app.app_context():
        moedas = Cryptocurrency.query.filter(Cryptocurrency.status != 'S').order_by(Cryptocurrency.name).all()
    return render_template('cryptos.html', moedas=moedas)

#----------------------  FIM ROTAS-------------------------
#****************************************************************
#----------------------  ATIVIDADE ROTA ADICIONAR TRANSAÇÃO-------------------------
#Pega preço atual da morda para preencher campos tela transsação
@app.route('/get_price/<int:cryptocurrency_id>', methods=['GET'])
def get_price(cryptocurrency_id):
    session = create_session()    
    # Busca o preço mais recente da moeda selecionada
    latest_price = session.query(Price.price).filter(Price.cryptocurrency_id == cryptocurrency_id).order_by(Price.timestamp.desc()).first()
    
    if latest_price:
        return jsonify({'price': latest_price[0]})
    else:
        return jsonify({'price': 0})

#---------------- Adicionar Carteira ------------------------
@app.route('/add_wallet', methods=['GET', 'POST'])
def add_wallet():
    session = create_session()
    try:
        formAddCarteiras = AddWalletForm()
        if formAddCarteiras.validate_on_submit():
            wallet_name = formAddCarteiras.nomeCarteira.data.upper()
            wallet_network = formAddCarteiras.redeCarteira.data.upper()
            with app.app_context():
                carteira = Wallet(user_id=1, name=wallet_name, network=wallet_network) #???remover user_id
                session.add(carteira)
                session.commit()
                flash(f'A carteira {(formAddCarteiras.nomeCarteira.data).upper()} foi adicionada com sucesso', 'alert-success')
    except Exception as e:
        flash(f'Erro ao tentar adicionar a carteira:\n{e}', 'alert-danger')
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('carteiras'))

#---------------- Remover Carteira ------------------------
@app.route('/delete_wallet', methods=['POST'])
def delete_wallet():
    session = create_session()
    try:
        # Obtém o ID da carteira a partir do formulário
        carteira_id = request.form.get('wallet_id')
        if carteira_id:
            with app.app_context():
                # Busca a carteira pelo ID
                carteira = session.query(Wallet).filter_by(id=carteira_id).first()
                if carteira:
                    # Atualiza o campo de status para 'S'
                    carteira.status = 'S'
                    session.commit()
                    flash(f'Carteira desativada com sucesso', 'alert-success')
    except Exception as e:
        flash(f'Erro ao tentar desativar a carteira:\n{e}', 'alert-danger')
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('carteiras'))

#---------------- Adicionar Moeda ------------------------
@app.route('/add_crypto', methods=['GET','POST'])
def add_crypto():
    session = create_session()
    try:
        formAddMoedas = AddCryptoForm()
        if formAddMoedas.validate_on_submit():
            cripto_name = formAddMoedas.nomeMoeda.data.upper()
            cripto_symbol = formAddMoedas.symbolMoeda.data.upper()
            with app.app_context():
                moeda = Cryptocurrency(name=cripto_name, symbol=cripto_symbol)
                session.add(moeda)
                session.commit()
                flash(f'A moeda {(formAddMoedas.nomeMoeda.data).upper()} foi adicionada com sucesso', 'alert-success')
    except Exception as e:
        flash(f'Erro ao tentar adicionar moeda:\n{e}', 'alert-danger')
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('moedas'))

#---------------- Remover Moeda ------------------------
@app.route('/delete_crypto', methods=['POST'])
def delete_crypto():
    session = create_session()
    try:
        # Obtém o ID da criptomoeda a partir do formulário
        crypto_id = request.form.get('crypto_id')
        if crypto_id:
            with app.app_context():
                # Busca a criptomoeda pelo ID
                moeda = session.query(Cryptocurrency).filter_by(id=crypto_id).first()
                if moeda:
                    # Atualiza o campo de status para 'S'
                    moeda.status = 'S'
                    session.commit()
                    flash(f'Moeda desativada com sucesso', 'alert-success')
        else:
            print("ID da criptomoeda não fornecido")
    except Exception as e:
        flash(f'Erro ao tentar desativar moeda:\n{e}', 'alert-danger')
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('moedas'))

# VER PARA ADICIONAR PREÇO MANUALMENTE!!!!!!!!!!!???????????????????????
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


#Atualiza os preços das moedas cadastradas pela API
@app.route('/update_prices', methods=['POST'])
def update_prices():
    try:
        with app.app_context():
            session = create_session()
            cryptocurrencies = session.query(Cryptocurrency).filter_by(status='N').all()
            for crypto in cryptocurrencies:
                price = get_crypto_price(COINMARKETCAP_API_KEY, crypto.symbol)
                if price is not None:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    crypto_price = Price(cryptocurrency_id=crypto.id, price=price, timestamp=timestamp)
                    session.add(crypto_price)
                    flash(f'Preços das moedas cadastradas atualizado com sucesso', 'alert-success')
            session.commit()
    except Exception as e:
        flash(f'Erro ao tentar atualizar os preços: {e}', 'alert-danger')
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

