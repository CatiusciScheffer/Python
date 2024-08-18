from flask import render_template, url_for, flash, request, redirect,jsonify
from sqlalchemy import func
from criptoControl.forms import TransacaoForm, AddWalletForm, AddCryptoForm
from criptoControl.models import db, User, Wallet, Cryptocurrency, WalletBalance, Transaction, Price
from criptoControl.api import get_crypto_price
from criptoControl import app
from datetime import datetime
from sqlalchemy.orm import sessionmaker



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
    formTransacoes.moedaTransacao.choices =[('', '')] + [(moeda.id, f"{moeda.name}({moeda.symbol})") for moeda in moedas]
    formTransacoes.moedaTaxa.choices = [('', '')] + [(moeda.id, f"{moeda.name}({moeda.symbol})") for moeda in moedas]
    formTransacoes.carteriaSaidaTransacao.choices = [('', '')] + [(carteira.id, carteira.name) for carteira in carteiras]
    formTransacoes.carteriaRecebimentoTransacao.choices = [('', '')] + [(carteira.id, carteira.name) for carteira in carteiras]
    
    return render_template('index.html', transacoes=transacoes, carteiras=carteiras, moedas=moedas, formTransacoes=formTransacoes, formAddCarteiras=formAddCarteiras, formAddMoedas=formAddMoedas)


#***** ROTA TRANSAÇÕES *****
@app.route('/transacoes')
def transacoes():
    transacoes = Transaction.query.order_by(Transaction.date).all()
    return render_template('transactions.html', transacoes=transacoes)



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
        COINMARKETCAP_API_KEY = '122d6732-65df-475c-8f1d-d7a95ab45bc5'#ver uma forma de salvar isso depois no banco
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
    print("Entrou na função add_transaction")
    try:
        # Coletando dados do formulário
        wallet_id = request.form.get('carteriaRecebimentoTransacao')
        crypto_trans_id = request.form.get('moedaTransacao')
        crypto_price = float(request.form.get('precoTransacao', 0))
        crypto_quantity = float(request.form.get('quantidadeTransacao', 0))
        transaction_total = float(request.form.get('totalTransacao', 0))
        
        fee_crypto_id = request.form.get('moedaTaxa')
        fee_price = float(request.form.get('precoTaxa', 0))
        fee_quantity = float(request.form.get('quantidadeTaxa', 0))
        fee_total = float(request.form.get('totalTaxa', 0))
        
        transaction_type = request.form.get('tipoTransacao')
        receiving_wallet_id = request.form.get('carteriaRecebimentoTransacao_id')

        # Imprimindo dados para depuração
        print(f"Dados recebidos: wallet={wallet_id}, crypto_trans_id={crypto_trans_id}, crypto_price={crypto_price}, crypto_quantity={crypto_quantity}, transaction_total={transaction_total}, fee_crypto_id={fee_crypto_id}, fee_price={fee_price}, fee_quantity={fee_quantity}, fee_total={fee_total}, transaction_type={transaction_type}, receiving_wallet_id={receiving_wallet_id}")
        
        with app.app_context():
            session = create_session()

            # Supondo que você tenha uma função de transação definida para realizar as operações
            if transaction_type == 'Compra':
                realizar_compra(session, wallet_id, crypto_trans_id, crypto_price, crypto_quantity, transaction_total, fee_crypto_id, fee_price, fee_quantity, fee_total)
            elif transaction_type == 'Venda':
                realizar_venda(session, wallet_id, crypto_trans_id, crypto_price, crypto_quantity, transaction_total, fee_crypto_id, fee_quantity, fee_total)
            elif transaction_type == 'Transferência':
                realizar_transferencia(session, wallet_id, receiving_wallet_id, crypto_trans_id, crypto_quantity, fee_crypto_id, fee_quantity, fee_total)
        
            session.commit()
            
    except Exception as e:
        flash(f'Erro ao tentar adicionar transação: {e}', 'alert-danger')
        session.rollback()
    
    return redirect(url_for('transacoes'))

# ***************** TRANSAÇÃO DE COMPRA  ******************#

def realizar_compra(session, wallet_id, crypto_trans_id, crypto_price, crypto_quantity, transaction_total, fee_crypto_id, fee_price, fee_quantity, fee_total):
    try:
        print(f'Realizando compra de {crypto_quantity} unidades de {crypto_trans_id} a {crypto_price} cada.')

        # Obter o saldo atual da carteira para a criptomoeda específica
        wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_trans_id).first()
        fee_wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=fee_crypto_id).first()
        '''
        if not wallet_balance:
            print(f'Saldo da criptomoeda {crypto_trans_id} não encontrado na carteira {wallet_id}.')
            flash(f'Saldo da criptomoeda {crypto_trans_id} não encontrado na carteira {wallet_id}.', 'alert-danger')
            return

        if not fee_wallet_balance:
            print(f'Saldo para a criptomoeda de taxa {fee_crypto_id} não encontrado.')
            flash(f'Saldo para a criptomoeda de taxa {fee_crypto_id} não encontrado.', 'alert-danger')
            return
        '''

        print(f'Saldo da moeda: {wallet_balance.balance}')
        print(f'Saldo da taxa: {fee_wallet_balance.balance}')

        if fee_wallet_balance.balance >= fee_total:
            print(f'MEUUUUUUUUUUUUUUUUUUUUU{fee_wallet_balance.balance}')
            print(f'Saldo suficiente para a taxa. Deduzindo {fee_quantity} da carteira de taxa.')

            # Atualizar o saldo da criptomoeda após a compra
            wallet_balance.balance += crypto_quantity

            # Deduz a taxa
            fee_wallet_balance.balance -= fee_quantity
            session.commit()  # Commit para garantir que a taxa é deduzida antes de atualizar o saldo

            transaction = Transaction(
                wallet_id=wallet_id,
                crypto_Trans_id=crypto_trans_id,
                crypto_price=crypto_price,
                crypto_quantity=crypto_quantity,
                transaction_total=transaction_total,
                type='Compra',
                fee_crypto_id=fee_crypto_id,
                fee_price=fee_price,
                fee_quantity=fee_quantity,
                fee_total=fee_total,
                receiving_wallet_id=wallet_id,
                date=datetime.now()
            )

            # Registrar a transação
            session.add(transaction)
            session.commit()
            print('Compra realizada com sucesso.')

        else:
            flash(f'Saldo Insuficiente para pagar a taxa na transação de compra.', 'alert-danger')

    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Compra: {e}', 'alert-danger')
        print(f'Erro na Transação de Compra: {e}')
        raise


#************************************************************************************************
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