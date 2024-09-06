from flask import render_template, url_for, flash, request, redirect, jsonify, session
from sqlalchemy import func, or_
from criptoControl.forms import TransactionsForm, AddWalletForm, AddCryptoForm
from criptoControl.models import db, Wallet, Cryptocurrency, WalletBalance, Transaction, Price
from criptoControl.api import get_crypto_payment_price
from criptoControl import app
from datetime import datetime
from sqlalchemy.orm import sessionmaker, joinedload



def create_session():
    return sessionmaker(bind=db.engine)()

#----------------------  INICIO ROTAS -------------------------
#***** ROTA INDEX *****
@app.route('/')
def index():
    formTransactions = TransactionsForm()
    formAddWallet = AddWalletForm()
    formAddCrypto = AddCryptoForm()
    session = create_session()

    try:        
        # Busca as informações no banco
        cons_transactions = session.query(Transaction).all()
        cons_wallets = session.query(Wallet).filter(Wallet.wallet_status=='N').all()
        cons_crypto = session.query(Cryptocurrency).filter(Cryptocurrency.crypto_status=='N').all()       
    finally:
        session.close()    
    return render_template('index.html', cons_transactions=cons_transactions, cons_wallets=cons_wallets, cons_crypto=cons_crypto, formTransactions=formTransactions, formAddWallet=formAddWallet, formAddCrypto=formAddCrypto)



#***** ROTA TRANSAÇÕES *****
@app.route('/transactions')
def transactions():
    session = create_session()
    try:
        cons_transactions = session.query(Transaction).options(
            joinedload(Transaction.payment_wallet),
            joinedload(Transaction.receiving_wallet),
            joinedload(Transaction.crypto_payment),
            joinedload(Transaction.crypto_receive),
            joinedload(Transaction.crypto_fee)
        ).all()
    finally:
        session.close()
    return render_template('transactions.html', cons_transactions=cons_transactions)


@app.route('/add_transactions')
def add_transactions(): 
    formTransactions = TransactionsForm()
    formAddWallet = AddWalletForm()
    formAddCrypto = AddCryptoForm()
    db_session = create_session()  # Renomeado para evitar conflito com flask.session

    try:        
        # Busca as informações no banco
        transactions = db_session.query(Transaction).all()
        wallets = db_session.query(Wallet).filter(Wallet.wallet_status=='N').all()
        cryptos = db_session.query(Cryptocurrency).filter(Cryptocurrency.crypto_status=='N').all()

        # Popular as informações do banco no HTML
        formTransactions.crypto_payment.choices = [('', '')] + [(crypto.crypto_id, f"{crypto.crypto_name}({crypto.crypto_symbol})") for crypto in cryptos]
        formTransactions.crypto_fee.choices = [('', '')] + [(crypto.crypto_id, f"{crypto.crypto_name}({crypto.crypto_symbol})") for crypto in cryptos]
        formTransactions.crypto_receive.choices = [('', '')] + [(crypto.crypto_id, f"{crypto.crypto_name}({crypto.crypto_symbol})") for crypto in cryptos]
        formTransactions.payment_wallet.choices = [('', '')] + [(wallet.wallet_id, wallet.wallet_name) for wallet in wallets]
        formTransactions.receiving_wallet.choices = [('', '')] + [(wallet.wallet_id, wallet.wallet_name) for wallet in wallets]

        # Verificar se existem dados armazenados na sessão para recuperar preenchimento
        if 'form_data' in session:
            form_data = session.pop('form_data')  # Use `session` directly from Flask
            
            # Preencher o formulário com os dados recuperados
            formTransactions.transaction_type.data = form_data.get('transaction_type')
            formTransactions.transaction_date.data = form_data.get('transaction_date')
            formTransactions.receiving_wallet.data = form_data.get('receiving_wallet_id')
            formTransactions.payment_wallet.data = form_data.get('payment_wallet_id')
            formTransactions.crypto_payment.data = form_data.get('crypto_payment_id')
            formTransactions.crypto_payment_price.data = form_data.get('crypto_payment_price')
            formTransactions.crypto_payment_quantity.data = form_data.get('crypto_payment_quantity')
            formTransactions.total_paid.data = form_data.get('total_paid')
            formTransactions.crypto_receive.data = form_data.get('crypto_receive_id')
            formTransactions.crypto_receive_price.data = form_data.get('crypto_receive_price')
            formTransactions.crypto_receive_quantity.data = form_data.get('crypto_receive_quantity')
            formTransactions.total_received.data = form_data.get('total_received')
            formTransactions.crypto_fee.data = form_data.get('crypto_fee_id')
            formTransactions.crypto_fee_price.data = form_data.get('crypto_fee_price')
            formTransactions.crypto_fee_quantity.data = form_data.get('crypto_fee_quantity')
            formTransactions.total_fee.data = form_data.get('total_fee')

    finally:
        db_session.close()  # Fechar a sessão do SQLAlchemy

    return render_template('add_transactions.html', transactions=transactions, wallets=wallets, cryptos=cryptos, formTransactions=formTransactions, formAddWallet=formAddWallet, formAddCrypto=formAddCrypto)


#***** ROTA PREÇOS *****
@app.route('/prices')
def prices():
    with app.app_context():
        session = create_session()
        
        # Subconsulta para obter o preço mais recente de cada criptomoeda
        subquery = (
            session.query(Price.price_crypto_id, func.max(Price.price_consult_datetime).label('latest_timestamp'))
            .group_by(Price.price_crypto_id)
            .subquery()
        )
        
        # Consulta principal para obter os preços mais recentes
        prices = (
            session.query(Price)
            .join(subquery, (Price.price_crypto_id == subquery.c.price_crypto_id) &
                                (Price.price_consult_datetime == subquery.c.latest_timestamp))
            .join(Cryptocurrency, Price.price_crypto_id == Cryptocurrency.crypto_id)
            .filter(Cryptocurrency.crypto_status == 'N')  # Corrigido para filtrar pelo status 'N'
            .all()
        )
    
    return render_template('prices.html', prices=prices)




#***** ROTA CARTEIRAS *****
@app.route('/wallets')
def wallets():
    with app.app_context():
        wallets = Wallet.query.filter(Wallet.wallet_status != 'S').order_by(Wallet.wallet_name).all()
    
    return render_template('wallets.html', wallets=wallets)


#***** ROTA MOEDAS *****
@app.route('/cryptos')
def cryptos():
    with app.app_context():
        cryptos = Cryptocurrency.query.filter(Cryptocurrency.crypto_status != 'S').order_by(Cryptocurrency.crypto_name).all()
    return render_template('cryptos.html', cryptos=cryptos)

#----------------------  FIM ROTAS-------------------------
#****************************************************************
#----------------------  ATIVIDADE ROTA ADICIONAR TRANSAÇÃO-------------------------
#Pega preço atual da morda para preencher campos tela transsação
@app.route('/get_price/<int:cryptocurrency_id>', methods=['GET'])
def get_price(cryptocurrency_id):
    session = create_session()    
    # Busca o preço mais recente da crypto selecionada
    latest_price = session.query(Price.price).filter(Price.price_crypto_id == cryptocurrency_id).order_by(Price.price_consult_datetime.desc()).first()
    
    if latest_price:
        return jsonify({'price': latest_price[0]})
    else:
        return jsonify({'price': 0})


#---------------- Adicionar Carteira ------------------------
@app.route('/add_wallet', methods=['GET', 'POST'])
def add_wallet():
    session = create_session()
    try:
        formAddWallet = AddWalletForm()
        if formAddWallet.validate_on_submit():
            wallet_name = formAddWallet.wallet_name.data.upper()
            wallet_network = formAddWallet.wallet_network.data.upper()
            with app.app_context():
                wallet = Wallet(wallet_user_id=1, wallet_name=wallet_name, wallet_network=wallet_network) #???remover user_id
                session.add(wallet)
                session.commit()
                flash(f'A Carteira {(formAddWallet.wallet_name.data).upper()} foi adicionada com sucesso', 'alert-success')
    except Exception as e:
        flash(f'Erro ao tentar adicionar a wallet:\n{e}', 'alert-danger')
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('wallets'))

#---------------- Remover Carteira ------------------------
@app.route('/delete_wallet', methods=['POST'])
def delete_wallet():
    session = create_session()
    try:
        # Obtém o ID da carteira a partir do formulário
        wallet_id = request.form.get('wallet_id')
        if wallet_id:
            with app.app_context():
                # Busca a carteira pelo ID
                wallet = session.query(Wallet).filter_by(wallet_id=wallet_id).first()
                
                if not wallet:
                    flash(f'Carteira não encontrada.', 'alert-danger')
                    return redirect(url_for('wallets'))

                # Verifica se há transações associadas à carteira
                wallet_in_transactions = session.query(Transaction).filter(
                    or_(
                        Transaction.payment_wallet_id == wallet_id,
                        Transaction.receiving_wallet_id == wallet_id
                    )
                ).first()

                if not wallet_in_transactions:
                    # Se não há transações associadas, deleta a carteira
                    session.delete(wallet)
                    session.commit()
                    flash(f'Carteira deletada com sucesso.', 'alert-success')
                else:
                    # Se há transações associadas, atualiza o status para 'S'
                    wallet.wallet_status = 'S'
                    session.commit()
                    flash(f'Carteira desativada pois já tiveram transações com ela.', 'alert-success')
        else:
            flash("ID da wallet não fornecido", 'alert-danger')
    except Exception as e:
        flash(f'Erro ao tentar desativar a wallet: {e}', 'alert-danger')
        session.rollback()
    finally:
        session.close()
    
    return redirect(url_for('wallets'))



#---------------- Adicionar Moeda ------------------------
@app.route('/add_crypto', methods=['GET','POST'])
def add_crypto():
    session = create_session()
    try:
        formAddCrypto = AddCryptoForm()
        if formAddCrypto.validate_on_submit():
            crypto_name = formAddCrypto.crypto_name.data.upper()
            crypto_symbol = formAddCrypto.crypto_symbol.data.upper()
            with app.app_context():
                crypto = Cryptocurrency(crypto_name=crypto_name, crypto_symbol=crypto_symbol)
                session.add(crypto)
                session.commit()
                flash(f'A Criptomoeda {(formAddCrypto.crypto_name.data).upper()} foi adicionada com sucesso', 'alert-success')
    except Exception as e:
        flash(f'Erro ao tentar adicionar crypto:\n{e}', 'alert-danger')
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('cryptos'))

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
                crypto = session.query(Cryptocurrency).filter_by(crypto_id=crypto_id).first()
                
                if not crypto:
                    flash(f'Moeda não encontrada.', 'alert-danger')
                    return redirect(url_for('cryptos'))

                # Verifica se há transações associadas à criptomoeda
                crypto_in_transaction = session.query(Transaction).filter(
                    or_(
                        Transaction.crypto_payment_id == crypto.crypto_id,
                        Transaction.crypto_receive_id == crypto.crypto_id,
                        Transaction.crypto_fee_id == crypto.crypto_id
                    )
                ).first()

                if not crypto_in_transaction:
                    # Se não há transações associadas, deleta a criptomoeda
                    session.delete(crypto)
                    session.commit()
                    flash(f'Moeda deletada com sucesso.', 'alert-success')
                else:
                    # Se há transações associadas, atualiza o status para 'S'
                    crypto.crypto_status = 'S'
                    session.commit()
                    flash(f'Moeda apenas desativada, pois tiveram transações com ela.', 'alert-success')
        else:
            flash("ID da criptomoeda não fornecido", 'alert-danger')
    except Exception as e:
        flash(f'Erro ao tentar desativar crypto:\n{e}', 'alert-danger')
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('cryptos'))


# VER PARA ADICIONAR PREÇO MANUALMENTE!!!!!!!!!!!???????????????????????
@app.route('/add_price', methods=['POST'])
def add_price():
    try:
        crypto_id = request.form['cryptocurrency_id']
        price = float(request.form['price'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with app.app_context():
            session = create_session()
            crypto_payment_price = Price(cryptocurrency_id=crypto_id, price=price, timestamp=timestamp)
            session.add(crypto_payment_price)
            session.commit()
    except Exception as e:
        print(f"Erro ao adicionar preço: {e}")
        session.rollback()
    return redirect(url_for('prices'))


#Atualiza os preços das cryptos cadastradas pela API
@app.route('/update_prices', methods=['POST'])
def update_prices():
    try:
        COINMARKETCAP_API_KEY = '122d6732-65df-475c-8f1d-d7a95ab45bc5'#ver uma forma de salvar isso depois no banco
        with app.app_context():
            session = create_session()
            crypto = session.query(Cryptocurrency).filter_by(crypto_status='N').all()
            for crypto in crypto:
                price = get_crypto_payment_price(COINMARKETCAP_API_KEY, crypto.crypto_symbol)
                if price is not None:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    crypto_price = Price(price_crypto_id=crypto.crypto_id, price=price, price_consult_datetime=timestamp)
                    session.add(crypto_price)
                    flash(f'Preços das cryptos cadastradas atualizado com sucesso', 'alert-success')
            session.commit()
    except Exception as e:
        flash(f'Erro ao tentar atualizar os preços: {e}', 'alert-danger')
        session.rollback()
    return redirect(url_for('prices'))


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    print("Entrou na função add_transaction")

    session = None
    
    try:
        # Dados gerais da transação
        transaction_type = request.form.get('transaction_type')
        transaction_date = request.form.get('transaction_date')
        
        # Dados carteiras da transação        
        receiving_wallet_id = request.form.get('receiving_wallet')
        payment_wallet_id = request.form.get('payment_wallet')
        
        # Dados das moedas pagadoras
        crypto_payment_id = request.form.get('crypto_payment')
        crypto_payment_price = request.form.get('crypto_payment_price')
        crypto_payment_quantity = request.form.get('crypto_payment_quantity')
        total_paid = request.form.get('total_paid')
        
        # Convertendo para float com verificação
        crypto_payment_price = float(crypto_payment_price) if crypto_payment_price else 0.0
        crypto_payment_quantity = float(crypto_payment_quantity) if crypto_payment_quantity else 0.0
        total_paid = float(total_paid) if total_paid else 0.0
        
        # Dados da moeda recebedora
        crypto_receive_id = request.form.get('crypto_receive')
        crypto_receive_price = request.form.get('crypto_receive_price')
        crypto_receive_quantity = request.form.get('crypto_receive_quantity')
        total_received = request.form.get('total_received')
        
        # Convertendo para float com verificação
        crypto_receive_price = float(crypto_receive_price) if crypto_receive_price else 0.0
        crypto_receive_quantity = float(crypto_receive_quantity) if crypto_receive_quantity else 0.0
        total_received = float(total_received) if total_received else 0.0

        # Dados da taxa
        crypto_fee_id = request.form.get('crypto_fee')
        crypto_fee_price = request.form.get('crypto_fee_price')
        crypto_fee_quantity = request.form.get('crypto_fee_quantity')
        total_fee = request.form.get('total_fee')
        
        # Convertendo para float com verificação
        crypto_fee_price = float(crypto_fee_price) if crypto_fee_price else 0.0
        crypto_fee_quantity = float(crypto_fee_quantity) if crypto_fee_quantity else 0.0
        total_fee = float(total_fee) if total_fee else 0.0                         

        # Cria a sessão
        with app.app_context():
            session = create_session()

            # Realizar operações baseadas no tipo de transação
            if transaction_type == 'Compra':
                realizar_compra(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type='Compra')
            elif transaction_type == 'Saldo':
                enter_balance(session, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, transaction_date)
            elif transaction_type == 'Venda':
                realizar_venda(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type='Venda')
            elif transaction_type == 'Transferência':
                realizar_transferencia(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type='Transferência')

    except Exception as e:
        if session is not None:
            session.rollback()
        flash(f'Erro ao tentar adicionar transação: {e}', 'alert-danger')
        print(f'Erro ao tentar adicionar transação: {e}')
    
    return redirect(url_for('add_transactions'))
    

#********     COMPRA    *******     COMPRA    ********
#armazenar dados do formulário na transação de compra
def store_data(transaction_type, receiving_wallet_id=None, payment_wallet_id=None,
               crypto_receive_id=None, crypto_receive_price=None, crypto_receive_quantity=None,
               total_received=None, crypto_payment_id=None, crypto_payment_price=None,
               crypto_payment_quantity=None, total_paid=None, crypto_fee_id=None,
               crypto_fee_price=None, crypto_fee_quantity=None, total_fee=None, transaction_date=None):
    session['form_data'] = {
        'transaction_type': transaction_type,
        'transaction_date': transaction_date,
        'payment_wallet_id': payment_wallet_id,
        'receiving_wallet_id': receiving_wallet_id,
        'crypto_payment_id': crypto_payment_id,
        'crypto_payment_price': crypto_payment_price,
        'crypto_payment_quantity': crypto_payment_quantity,
        'total_paid': total_paid,
        'crypto_receive_id': crypto_receive_id,
        'crypto_receive_price': crypto_receive_price,
        'crypto_receive_quantity': crypto_receive_quantity,
        'total_received': total_received,
        'crypto_fee_id': crypto_fee_id,
        'crypto_fee_price': crypto_fee_price,
        'crypto_fee_quantity': crypto_fee_quantity,
        'total_fee': total_fee
    }


def check_mandatory_fields_in_purchase(payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date=None):

    if not all([payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type]):
        store_data(
            transaction_type=transaction_type,
            payment_wallet_id=payment_wallet_id,
            receiving_wallet_id=receiving_wallet_id,
            crypto_payment_id=crypto_payment_id,
            crypto_payment_price=crypto_payment_price,
            crypto_payment_quantity=crypto_payment_quantity,
            total_paid=total_paid,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            crypto_fee_id=crypto_fee_id,
            crypto_fee_price=crypto_fee_price,
            crypto_fee_quantity=crypto_fee_quantity,
            total_fee=total_fee,
            transaction_date=transaction_date
        )
        flash('Preencha/Verifique todos os campos!', 'alert-danger')
        return redirect(url_for('add_transactions'))

    if not transaction_date:
        store_data(
            transaction_type=transaction_type,
            payment_wallet_id=payment_wallet_id,
            receiving_wallet_id=receiving_wallet_id,
            crypto_payment_id=crypto_payment_id,
            crypto_payment_price=crypto_payment_price,
            crypto_payment_quantity=crypto_payment_quantity,
            total_paid=total_paid,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            crypto_fee_id=crypto_fee_id,
            crypto_fee_price=crypto_fee_price,
            crypto_fee_quantity=crypto_fee_quantity,
            total_fee=total_fee
        )
        flash('Preencha data!', 'alert-danger')
        return redirect(url_for('add_transactions'))



def realizar_compra(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type):
    
    try:
        print('Realizando Compra.')

        # Verificar campos obrigatórios
        redirect_result_com = check_mandatory_fields_in_purchase(payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date)
        if redirect_result_com:
            print('Campo vazio')
            return redirect_result_com
        
        # Carteira de pagamento
        payment_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_payment_id).first()
        # Carteira de recebimento
        receiving_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_receive_id).first()

        print(f'payment_wallet: {payment_wallet}, receiving_wallet: {receiving_wallet}')

        # Consulta se tem saldo suficiente para a taxa na carteira da transação
        fee_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, 
            balance_crypto_id=crypto_fee_id
        ).first()

        # Consulta saldo da moeda pagadora na carteira da transação
        crypto_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, 
            balance_crypto_id=crypto_payment_id
        ).first()

        saldo_pagto_fee_tran = False

        if fee_wallet_balance and crypto_wallet_balance:
            saldo_pagto_fee_tran = (fee_wallet_balance.balance >= crypto_fee_quantity) and (crypto_wallet_balance.balance >= crypto_payment_quantity)

        # Verifica se tem saldo da crypto da taxa
        if saldo_pagto_fee_tran:
            print(f'Saldo da taxa: {fee_wallet_balance.balance}')
            print(f'Saldo suficiente para a taxa. Deduzindo {crypto_fee_quantity} da wallet de taxa e {crypto_payment_quantity} da wallet de pagamento.')

            # Criar a transação
            transaction = Transaction(
                transaction_type=transaction_type, 
                transaction_date=datetime.strptime(transaction_date, '%Y-%m-%d'), 
                payment_wallet_id=payment_wallet_id, 
                receiving_wallet_id=receiving_wallet_id, 
                crypto_payment_id=crypto_payment_id, 
                crypto_payment_price=crypto_payment_price, 
                crypto_payment_quantity=crypto_payment_quantity, 
                total_paid=total_paid, 
                crypto_receive_id=crypto_receive_id, 
                crypto_receive_price=crypto_receive_price, 
                crypto_receive_quantity=crypto_receive_quantity, 
                total_received=total_received, 
                crypto_fee_id=crypto_fee_id, 
                crypto_fee_price=crypto_fee_price, 
                crypto_fee_quantity=crypto_fee_quantity, 
                total_fee=total_fee
            )
            
            print(f'Transaction: {transaction}')

            # Registrar a transação
            session.add(transaction)

            # Atualizar saldo das carteiras
            if fee_wallet_balance:
                fee_wallet_balance.balance -= crypto_fee_quantity

            if crypto_wallet_balance:
                crypto_wallet_balance.balance -= crypto_payment_quantity

            if receiving_wallet: # carteira de recebimento existe
                receiving_wallet.balance += crypto_receive_quantity
            else:
                # Se a crypto não existe em balance, insere
                novo_saldo = WalletBalance(
                    balance_wallet_id=receiving_wallet_id,
                    balance_crypto_id=crypto_receive_id,
                    balance=crypto_receive_quantity
                )
                session.add(novo_saldo)
            
            session.commit()

            flash('Transação realizada com sucesso!', 'alert-success')
        else:
            flash('Transação não realizada: Saldo Insuficiente!', 'alert-danger')

    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Compra: {e}', 'alert-danger')
        raise


#********     SALDO    *******     SALDO    ********
#verifica campos obrigatórios
def check_mandatory_fields_in_balance(receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, transaction_date=None):

    if not all([receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received]):
        store_data(
            transaction_type='Saldo',
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            transaction_date=transaction_date
        )
        flash('Preencha/Verifique todos os campos!', 'alert-danger')
        return redirect(url_for('add_transactions'))

    if not transaction_date:
        store_data(
            transaction_type='Saldo',
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received
        )
        flash('Preencha data!', 'alert-danger')
        return redirect(url_for('add_transactions'))
    

def enter_balance(db_session, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, transaction_date):
    try:
        # Verificar campos obrigatórios
        redirect_result = check_mandatory_fields_in_balance(receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, transaction_date)
        if redirect_result:
            return redirect_result
        
        # Obter o saldo atual da carteira para a criptomoeda específica
        balance_wallet = db_session.query(WalletBalance).filter_by(balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_receive_id).first()

        # Criar a transação
        transaction = Transaction(
            transaction_type='Saldo',
            transaction_date=datetime.strptime(transaction_date, '%Y-%m-%d'),
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received
        )

        db_session.add(transaction)
        db_session.commit()

        # Atualizar o saldo da criptomoeda após a compra
        if balance_wallet:
            balance_wallet.balance += crypto_receive_quantity
        else:
            novo_saldo = WalletBalance(
                balance_wallet_id=receiving_wallet_id,
                balance_crypto_id=crypto_receive_id,
                balance=crypto_receive_quantity
            )
            db_session.add(novo_saldo)
        
        db_session.commit()

        flash('Saldo adicionado com sucesso!', 'alert-success')
    except Exception as e:
        db_session.rollback()
        flash(f'Erro na Transação de Compra: {e}', 'alert-danger')
        raise


#************************************************************************************************
def realizar_venda(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type):
    try:
        print('Realizando Venda.')

        # Verificar campos obrigatórios
        redirect_result_com = check_mandatory_fields_in_purchase(payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date)
        if redirect_result_com:
            return redirect_result_com
        
        # Carteira de pagamento
        payment_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_payment_id).first()
        # Carteira de recebimento
        receiving_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_payment_id).first()

        print(f'payment_wallet: {payment_wallet}, receiving_wallet: {receiving_wallet}')

        # Consulta se tem saldo suficiente para a taxa na carteira da transação
        fee_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, 
            balance_crypto_id=crypto_fee_id
        ).first()

        # Consulta saldo da moeda pagadora na carteira da transação
        crypto_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, 
            balance_crypto_id=crypto_payment_id
        ).first()

        saldo_pagto_fee_tran = False

        if crypto_payment_id != crypto_fee_id:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_fee_tran = (fee_wallet_balance.balance >= crypto_fee_quantity) and (crypto_wallet_balance.balance >= crypto_payment_quantity)
        else:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_fee_tran = (fee_wallet_balance.balance + crypto_wallet_balance.balance >= crypto_fee_quantity + crypto_payment_quantity)

        # Verifica se tem saldo da crypto da taxa
        if saldo_pagto_fee_tran:
            print(f'Saldo da taxa: {fee_wallet_balance.balance if fee_wallet_balance else 0}')
            print(f'Saldo suficiente para a taxa. Deduzindo {crypto_fee_quantity} da wallet de taxa.')

            # Criar a transação
            transaction = Transaction(
                transaction_type=transaction_type, 
                transaction_date=datetime.strptime(transaction_date, '%Y-%m-%d'), 
                payment_wallet_id=payment_wallet_id, 
                receiving_wallet_id=receiving_wallet_id, 
                crypto_payment_id=crypto_payment_id, 
                crypto_payment_price=crypto_payment_price, 
                crypto_payment_quantity=crypto_payment_quantity, 
                total_paid=total_paid, 
                crypto_receive_id=crypto_receive_id, 
                crypto_receive_price=crypto_receive_price, 
                crypto_receive_quantity=crypto_receive_quantity, 
                total_received=total_received, 
                crypto_fee_id=crypto_fee_id, 
                crypto_fee_price=crypto_fee_price, 
                crypto_fee_quantity=crypto_fee_quantity, 
                total_fee=total_fee
            )
            
            print(f'Transaction: {transaction}')

            # Registrar a transação
            session.add(transaction)

            if fee_wallet_balance: # tem saldo para taxa
                fee_wallet_balance.balance -= crypto_fee_quantity

            if crypto_wallet_balance: # tem saldo para pagamento
                crypto_wallet_balance.balance -= crypto_payment_quantity

            if receiving_wallet: # carteira de recebimento existe
                receiving_wallet.balance += crypto_receive_quantity
            else:
                # Se a crypto não existe em balance, insere
                novo_saldo = WalletBalance(
                    balance_wallet_id=receiving_wallet_id,
                    balance_crypto_id=crypto_receive_id,
                    balance=crypto_receive_quantity
                )
                session.add(novo_saldo)
            
            session.commit()

            flash('Transação realizada com sucesso!', 'alert-success')
        else:
            flash('Transação não realizada: Saldo Insuficiente!', 'alert-danger')

    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Venda: {e}', 'alert-danger')
        raise

#************* REALIZANDO TRANSFERÊNCIA *******************
def check_mandatory_fields_in_transf(
    payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received,
    crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date=None
):
    # Verificar se todos os campos obrigatórios estão preenchidos
    if not all([
        payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received,
        crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type
    ]):
        store_data(
            transaction_type=transaction_type,
            payment_wallet_id=payment_wallet_id,
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            crypto_fee_id=crypto_fee_id,
            crypto_fee_price=crypto_fee_price,
            crypto_fee_quantity=crypto_fee_quantity,
            total_fee=total_fee,
            transaction_date=transaction_date
        )
        flash('Preencha/Verifique todos os campos!', 'alert-danger')
        return redirect(url_for('add_transactions'))

    if not transaction_date:
        store_data(
            transaction_type=transaction_type,
            payment_wallet_id=payment_wallet_id,
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            crypto_fee_id=crypto_fee_id,
            crypto_fee_price=crypto_fee_price,
            crypto_fee_quantity=crypto_fee_quantity,
            total_fee=total_fee
        )
        flash('Preencha a data!', 'alert-danger')
        return redirect(url_for('add_transactions'))


def realizar_transferencia(
    session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity,
    total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type
):
    try:
        # Verificar campos obrigatórios
        redirect_result_com = check_mandatory_fields_in_transf(
            payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received,
            crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date
        )
        if redirect_result_com:
            return redirect_result_com
        
        # Verifica o saldo da carteira de pagamento para a criptomoeda de pagamento e a taxa
        payment_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_receive_id
        ).first()
        
        fee_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_fee_id
        ).first()

        # Verificar se há saldo suficiente para a taxa e a quantidade a ser transferida
        if payment_wallet_balance and fee_wallet_balance and payment_wallet_balance.balance >= (crypto_receive_quantity + crypto_fee_quantity) and fee_wallet_balance.balance >= crypto_fee_quantity:
            # Deduz a quantidade total (transferência + taxa) da carteira de pagamento
            payment_wallet_balance.balance -= crypto_receive_quantity
            fee_wallet_balance.balance -= crypto_fee_quantity

            # Cria a transação
            transaction = Transaction(
                transaction_type=transaction_type, 
                transaction_date=datetime.strptime(transaction_date, '%Y-%m-%d'), 
                payment_wallet_id=payment_wallet_id, 
                receiving_wallet_id=receiving_wallet_id, 
                crypto_receive_id=crypto_receive_id, 
                crypto_receive_price=crypto_receive_price, 
                crypto_receive_quantity=crypto_receive_quantity, 
                total_received=total_received, 
                crypto_fee_id=crypto_fee_id, 
                crypto_fee_price=crypto_fee_price, 
                crypto_fee_quantity=crypto_fee_quantity, 
                total_fee=total_fee
            )
            
            # Registra a transação
            session.add(transaction)
            
            # Atualiza a carteira de recebimento
            wallet_balance_receb = session.query(WalletBalance).filter_by(
                balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_receive_id
            ).first()
            if wallet_balance_receb:
                wallet_balance_receb.balance += crypto_receive_quantity
            else:
                novo_recebimento_trans = WalletBalance(
                    balance_wallet_id=receiving_wallet_id,
                    balance_crypto_id=crypto_receive_id,
                    balance=crypto_receive_quantity
                )
                session.add(novo_recebimento_trans)

            # Commit das mudanças
            session.commit()
            flash('Transação realizada com sucesso!', 'alert-success')
        
        else:
            flash('Transação não realizada: Saldo Insuficiente!', 'alert-danger')
            session.rollback()
            
    except Exception as e:
        flash(f'Erro ao realizar transferência: {e}', 'alert-danger')
        session.rollback()
        raise




@app.route('/delete_transacao', methods=['POST'])
def delete_transaction():
    session = create_session()
    try:
        # Obtém o ID da transação a partir do formulário
        transacao_id = request.form.get('transacao_id')
        if transacao_id:
            with app.app_context():
                # Busca a transação pelo ID
                transacao = session.query(Transaction).filter_by(transactions_id=transacao_id).first()
                if transacao:
                    wallet_id_saida = transacao.payment_wallet_id
                    wallet_id_recebimento = transacao.receiving_wallet_id
                    crypto_payment_id = transacao.crypto_payment_id
                    crypto_fee_id = transacao.crypto_fee_id
                    crypto_payment_quantity = transacao.crypto_payment_quantity
                    crypto_fee_quantity = transacao.crypto_fee_quantity

                    # Verifica se existe saldo suficiente
                    wallet_balance = None
                    fee_wallet_balance = None
                    
                    # Lógica para verificar se há saldo suficiente para reverter a transação
                    if crypto_fee_id != crypto_payment_id:
                        # Verifica se tem saldo para a crypto transferida
                        wallet_balance = session.query(WalletBalance).filter_by(
                            payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_payment_id
                        ).filter(WalletBalance.balance >= crypto_payment_quantity).first()
                        
                        # Verifica se tem saldo suficiente para a taxa
                        if transacao.transaction_type != 'Saldo':
                            fee_wallet_balance = session.query(WalletBalance).filter_by(
                                payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_fee_id
                            ).filter(WalletBalance.balance >= crypto_fee_quantity).first()
                    else:
                        # Verifica se tem saldo para a crypto transferida junto com a taxa
                        wallet_balance = session.query(WalletBalance).filter_by(
                            payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_payment_id
                        ).filter(WalletBalance.balance >= (crypto_payment_quantity + crypto_fee_quantity)).first()
                        
                        if transacao.transaction_type != 'Saldo':
                            fee_wallet_balance = wallet_balance

                    # Busca o saldo da wallet de recebimento para venda
                    wallet_balance_receive = session.query(WalletBalance).filter_by(
                        payment_wallet_id=wallet_id_recebimento, cryptocurrency_id=crypto_payment_id
                    ).first()             

                    # Reverter saldo de acordo com o tipo de transação
                    if transacao.transaction_type == 'Compra':                       
                        if wallet_balance and fee_wallet_balance:
                            wallet_balance.balance -= crypto_payment_quantity
                            fee_wallet_balance.balance += crypto_fee_quantity
                    
                    elif transacao.transaction_type == 'Venda':
                        if wallet_balance and fee_wallet_balance:
                            wallet_balance.balance += crypto_payment_quantity
                            wallet_balance_receive.balance -= crypto_payment_quantity
                            fee_wallet_balance.balance += crypto_fee_quantity

                    elif transacao.transaction_type == 'Transferência':
                        if wallet_balance and fee_wallet_balance:
                            wallet_balance.balance += crypto_payment_quantity
                            wallet_balance_receive.balance -= crypto_payment_quantity
                            fee_wallet_balance.balance += crypto_fee_quantity

                    elif transacao.transaction_type == 'Saldo':
                        if wallet_balance:
                            wallet_balance.balance -= crypto_receive_quantity 

                    # Se todos os saldos foram revertidos corretamente
                    if wallet_balance and (fee_wallet_balance or transacao.transaction_type == 'Saldo'):
                        session.delete(transacao)
                        session.commit()
                        flash('Transação deletada com sucesso e saldos atualizados', 'alert-success')
                    else:
                        flash('Erro ao tentar deletar Transação: saldo insuficiente ou erro ao atualizar saldos', 'alert-danger')
                        session.rollback()

    except Exception as e:
        flash(f'Erro ao tentar deletar Transação:\n{e}', 'alert-danger')
        session.rollback()
    finally:
        session.close()
    return redirect(url_for('transactions'))









# ************ MOSTRAR SALDOS DE MOEDA POR CARTERIA ****************
@app.route('/wallet_summary')
def wallet_summary():
    # Obtém os dados de todas as carteiras
    vw_saldos, total_valor = get_wallet_summary()
    
    # Renderiza o template passando os dados
    return render_template('wallet_summary.html', saldos=vw_saldos, total_valor=total_valor)


def get_wallet_summary():
    # Subconsulta para obter o preço mais recente
    latest_prices_subquery = (
        db.session.query(
            Price.price_crypto_id,
            func.max(Price.price_consult_datetime).label('latest_timestamp')
        )
        .group_by(Price.price_crypto_id)
        .subquery()
    )
    
    # Consulta principal
    query = (
        db.session.query(
            Wallet.wallet_name.label('carteira'),
            Cryptocurrency.crypto_name.label('crypto'),
            WalletBalance.balance.label('quantidade'),
            Price.price.label('preço'),
            (WalletBalance.balance * Price.price).label('valor')
        )
        .join(WalletBalance, Wallet.wallet_id == WalletBalance.balance_wallet_id)
        .join(Cryptocurrency, Cryptocurrency.crypto_id == WalletBalance.balance_crypto_id)
        .join(Price, Price.price_id == Cryptocurrency.crypto_id)
        .join(latest_prices_subquery, 
               (Price.price_crypto_id == latest_prices_subquery.c.price_crypto_id) &
               (Price.price_consult_datetime == latest_prices_subquery.c.latest_timestamp))
        .order_by(Wallet.wallet_name)
        .all()
    )
    
    # Calcular a soma da coluna 'valor'
    total_valor = sum(row.valor for row in query)
    
    # Retornar os resultados como uma lista de dicionários e a soma total
    return [{
        'carteira': row.carteira,
        'crypto': row.crypto,
        'quantidade': row.quantidade,
        'preço': row.preço,
        'valor': row.valor
    } for row in query], total_valor

# ------ FIM _____  MOSTRAR SALDOS DE MOEDA POR CARTERIA ---------------