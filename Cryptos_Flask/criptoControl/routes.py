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
        #formTransacao = TransacaoForm()
        
        #wallet_id = formTransacao.carteriaSaidaTransacao.data#com isso não funciona saldo e compra
        wallet_id = request.form.get('carteriaRecebimentoTransacao')
        wallet_id_saida = request.form.get('carteriaSaidaTransacaoId')
        crypto_trans_id = request.form.get('moedaTransacao')
        crypto_price = float(request.form.get('precoTransacao', 0))
        crypto_quantity = float(request.form.get('quantidadeTransacao', 0))
        transaction_total = float(request.form.get('totalTransacao', 0))
        
        #fee_crypto_id = request.form.get('moedaTaxa')
        #fee_price = float(request.form.get('precoTaxa', 0))
        #fee_quantity = float(request.form.get('quantidadeTaxa', 0))
        #fee_total = float(request.form.get('totalTaxa', 0))
        
        transaction_type = request.form.get('tipoTransacao')
        receiving_wallet_id = request.form.get('carteriaRecebimentoTransacao_id')

        # Cria a sessão
        with app.app_context():
            session = create_session()

            # Supondo que você tenha uma função de transação definida para realizar as operações
            if transaction_type == 'Compra':
                realizar_compra(session, wallet_id, crypto_trans_id, crypto_price, crypto_quantity, transaction_total)
            elif transaction_type == 'Saldo':
                inserir_saldo(session, wallet_id, crypto_trans_id, crypto_price, crypto_quantity, transaction_total)
            elif transaction_type == 'Venda':
                realizar_venda(session, crypto_trans_id, crypto_price, crypto_quantity, transaction_total)
            elif transaction_type == 'Transferência':
                realizar_transferencia(session, wallet_id, receiving_wallet_id, crypto_trans_id, crypto_quantity)
        
            session.commit()
            
    except Exception as e:
        if session is not None:
            session.rollback()  # Apenas tenta fazer o rollback se a sessão foi criada
        flash(f'Erro ao tentar adicionar transação: {e}', 'alert-danger')
        print(f'Erro ao tentar adicionar transação: {e}')  # Adicionado para ajudar na depuração
    
    return redirect(url_for('transacoes'))


# ***************** TRANSAÇÃO DE COMPRA  ******************#

def realizar_compra(session, wallet_id, crypto_trans_id, crypto_price, crypto_quantity, transaction_total):
    fee_crypto_id = request.form.get('moedaTaxa')
    fee_price = float(request.form.get('precoTaxa', 0))
    fee_quantity = float(request.form.get('quantidadeTaxa', 0))
    fee_total = float(request.form.get('totalTaxa', 0))
    try:
        print(f'Realizando compra de {crypto_quantity} unidades de {crypto_trans_id} a {crypto_price} cada.')

        # consulta se a moeda da transação já existe
        wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_trans_id).first()
        
        # consulta se tem saldo suficiente para a taxa 
        fee_wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=fee_crypto_id).filter(WalletBalance.balance > fee_quantity).first()

        #verifica se tem saldo da moeda da taxa 
        if fee_wallet_balance is not None:
            print(f'Saldo da taxa: {fee_wallet_balance.balance}')
            print(f'Saldo suficiente para a taxa. Deduzindo {fee_quantity} da carteira de taxa.')

            if wallet_balance is not None:
                # se a moeda já existe em balance, soma
                wallet_balance.balance += crypto_quantity
            else:
                # se a moeda não existe em balance, insere
                novo_saldo = WalletBalance(
                    wallet_id=wallet_id,
                    cryptocurrency_id=crypto_trans_id,
                    balance=crypto_quantity
                )
                session.add(novo_saldo)

            # Deduz a taxa
            fee_wallet_balance.balance -= fee_quantity

            # Criar a transação
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

    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Compra: {e}', 'alert-danger')
        print(f'Erro na Transação de Compra: {e}')
        raise

#************************************************************************************************

def inserir_saldo(session, wallet_id, crypto_trans_id, crypto_price, crypto_quantity, transaction_total):
    try:
        print(f'Inserindo Saldo {crypto_quantity} unidades de {crypto_trans_id} a {crypto_price} cada.')

        # Obter o saldo atual da carteira para a criptomoeda específica
        wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_trans_id).first()
        
        print('Taxa zero, logo inserção de saldo')
        # Atualizar o saldo da criptomoeda após a compra
        if wallet_balance is not None:
            # Atualiza o saldo existente
            wallet_balance.balance += crypto_quantity            
        else:
            # Cria um novo registro em WalletBalance
            novo_saldo = WalletBalance(
                wallet_id=wallet_id,
                cryptocurrency_id=crypto_trans_id,
                balance=crypto_quantity
            )
            session.add(novo_saldo)

        # Criar a transação
        transaction = Transaction(
            wallet_id=wallet_id,
            crypto_Trans_id=crypto_trans_id,
            crypto_price=crypto_price,
            crypto_quantity=crypto_quantity,
            transaction_total=transaction_total,
            type='Saldo',
            fee_crypto_id='',
            fee_price=0.0,
            fee_quantity=0.0,
            fee_total=0.0,
            receiving_wallet_id=wallet_id,
            date=datetime.now()
        )

        session.add(transaction)
        session.commit()
        print('Compra realizada com sucesso.')

    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Compra: {e}', 'alert-danger')
        print(f'Erro na Transação de Compra: {e}')
        raise

#************************************************************************************************
def realizar_venda(session, crypto_trans_id, crypto_price, crypto_quantity, transaction_total):
    
    wallet_id_saida = request.form.get('carteriaSaidaTransacaoId')
    fee_crypto_id = request.form.get('moedaTaxa')
    fee_price = float(request.form.get('precoTaxa', 0))
    fee_quantity = float(request.form.get('quantidadeTaxa', 0))
    fee_total = float(request.form.get('totalTaxa', 0))
    try:
        print(f'Realizando venda de {crypto_quantity} unidades da moeda id {crypto_trans_id} a um preço de {crypto_price} cada.')

        # consulta se tem saldo para moeda vendida
        wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id_saida, cryptocurrency_id=crypto_trans_id).filter(WalletBalance.balance > crypto_quantity).first()
        
        # consulta se tem saldo suficiente para a taxa 
        fee_wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id_saida, cryptocurrency_id=fee_crypto_id).filter(WalletBalance.balance > fee_quantity).first()

        print(f'wallet_id: {wallet_id_saida}')
        print(f'crypto_trans_id: {crypto_trans_id}')
        print(f'fee_crypto_id: {fee_crypto_id}')

        #verifica se tem saldo das moedas 
        if (wallet_balance is not None) and (fee_wallet_balance is not None):
            print(f'Saldo da taxa: {fee_wallet_balance.balance}')
            print(f'Saldo da moeda vendida: {wallet_balance.balance}')

            # Deduz moeda vendida
            wallet_balance.balance -= crypto_quantity 
            
            # Deduz a taxa
            fee_wallet_balance.balance -= fee_quantity 

            # Criar a transação
            transaction = Transaction(
                wallet_id=wallet_id_saida,
                crypto_Trans_id=crypto_trans_id,
                crypto_price=crypto_price,
                crypto_quantity=crypto_quantity,
                transaction_total=transaction_total,
                type='Venda',
                fee_crypto_id=fee_crypto_id,
                fee_price=fee_price,
                fee_quantity=fee_quantity,
                fee_total=fee_total,
                date=datetime.now()
            )

            # Registrar a transação
            session.add(transaction)

            # Força a detecção das mudanças antes do commit
            session.flush()

            # Commit das mudanças
            session.commit()
            print('Venda realizada com sucesso.')

    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Venda: {e}', 'alert-danger')
        print(f'Erro na Transação de Venda: {e}')
        raise



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