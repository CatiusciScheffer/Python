from flask import Blueprint, render_template, url_for, flash, request, redirect, session, jsonify
from criptoControl.forms import TransactionsForm, AddWalletForm, AddCryptoForm
from criptoControl.models import db, Wallet, Cryptocurrency, WalletBalance, Transaction, Price, User
from flask_login import current_user, login_required
from sqlalchemy.orm import sessionmaker, joinedload
from datetime import datetime


transaction_bp = Blueprint('transaction', __name__)

def create_session():
    return sessionmaker(bind=db.engine)()


@transaction_bp.route('/transactions')
@login_required
def transactions():
    # Cria uma nova sessão do banco de dados
    session = create_session()
    
    try:
        user_id = current_user.user_id  
        
        cons_transactions = session.query(Transaction).options(
            joinedload(Transaction.payment_wallet),
            joinedload(Transaction.receiving_wallet),
            joinedload(Transaction.crypto_payment),
            joinedload(Transaction.crypto_receive),
            joinedload(Transaction.crypto_fee)
        ).join(
            Transaction.receiving_wallet
        ).filter(
            Wallet.wallet_user_id == user_id
        ).all()
    finally:
        # Garante que a sessão seja fechada corretamente
        session.close()

    # Renderiza o template com as transações
    return render_template('operacoes/transactions.html', cons_transactions=cons_transactions)


#Pega preço atual da morda para preencher campos tela transsação
@transaction_bp.route('/get_price/<int:cryptocurrency_id>', methods=['GET'])
def get_price(cryptocurrency_id):
    session = create_session()    
    # Busca o preço mais recente da crypto selecionada
    latest_price = session.query(Price.price).filter(Price.price_crypto_id == cryptocurrency_id).order_by(Price.price_consult_datetime.desc()).first()
    
    if latest_price:
        return jsonify({'price': latest_price[0]})
    else:
        return jsonify({'price': 0})
    

@transaction_bp.route('/add_transactions')
@login_required
def add_transactions(): 
    formTransactions = TransactionsForm()
    formAddWallet = AddWalletForm()
    formAddCrypto = AddCryptoForm()
    db_session = create_session()  # Renomeado para evitar conflito com flask.session

    try:        
        # Busca as informações no banco
        transactions = db_session.query(Transaction).all()
        wallets = db_session.query(Wallet).filter(
            Wallet.wallet_status=='N',
            Wallet.wallet_user_id == current_user.user_id
        ).all()
        cryptos = db_session.query(Cryptocurrency).filter(Cryptocurrency.crypto_status=='N').order_by(Cryptocurrency.crypto_symbol).all()

        # Popular as informações do banco no HTML
        formTransactions.crypto_payment.choices = [('', '')] + [(crypto.crypto_id, f"{crypto.crypto_symbol} - ({crypto.crypto_name})") for crypto in cryptos]
        
        formTransactions.crypto_fee.choices = [('', '')] + [(crypto.crypto_id, f"{crypto.crypto_symbol} - ({crypto.crypto_name})") for crypto in cryptos]
        
        formTransactions.crypto_receive.choices = [('', '')] + [(crypto.crypto_id, f"{crypto.crypto_symbol} - ({crypto.crypto_name})") for crypto in cryptos]
        
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

    return render_template('operacoes/add_transactions.html', transactions=transactions, wallets=wallets, cryptos=cryptos, formTransactions=formTransactions, formAddWallet=formAddWallet, formAddCrypto=formAddCrypto)


# Função normalize_decimal (exemplo)
def normalize_decimal(value):
    """Função para substituir vírgulas por pontos em valores numéricos."""
    if isinstance(value, str):
        return value.replace(',', '.')
    return value

@transaction_bp.route('/add_transaction', methods=['POST'])
def add_transaction():
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
        
        # Normalizando e convertendo para float
        crypto_payment_price = float(normalize_decimal(crypto_payment_price)) if crypto_payment_price else 0.0
        crypto_payment_quantity = float(normalize_decimal(crypto_payment_quantity)) if crypto_payment_quantity else 0.0
        total_paid = float(normalize_decimal(total_paid)) if total_paid else 0.0
        
        # Dados da moeda recebedora
        crypto_receive_id = request.form.get('crypto_receive')
        crypto_receive_price = request.form.get('crypto_receive_price')
        crypto_receive_quantity = request.form.get('crypto_receive_quantity')
        total_received = request.form.get('total_received')
        
        # Normalizando e convertendo para float
        crypto_receive_price = float(normalize_decimal(crypto_receive_price)) if crypto_receive_price else 0.0
        crypto_receive_quantity = float(normalize_decimal(crypto_receive_quantity)) if crypto_receive_quantity else 0.0
        total_received = float(normalize_decimal(total_received)) if total_received else 0.0


        # Dados da taxa
        crypto_fee_id = request.form.get('crypto_fee')
        crypto_fee_price = request.form.get('crypto_fee_price')
        crypto_fee_quantity = request.form.get('crypto_fee_quantity')
        total_fee = request.form.get('total_fee')
        
        # Normalizando e convertendo para float
        crypto_fee_price = float(normalize_decimal(crypto_fee_price)) if crypto_fee_price else 0.0
        crypto_fee_quantity = float(normalize_decimal(crypto_fee_quantity)) if crypto_fee_quantity else 0.0
        total_fee = float(normalize_decimal(total_fee)) if total_fee else 0.0                         

        # Cria a sessão
        session = create_session()

        # Realizar operações baseadas no tipo de transação
        if transaction_type == 'Compra':
            realizar_compra(session, transaction_date, payment_wallet_id, receiving_wallet_id,crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid,crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received,crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee,transaction_type='Compra')
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
    
    return redirect(url_for('transaction.add_transactions'))

    

#********     COMPRA    *******     COMPRA    ********
#armazenar dados do formulário de transações para qualquer transação
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

#esta função é usada na transação da compra e da venda
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
        return redirect(url_for('transaction.add_transactions'))

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
        return redirect(url_for('transaction.add_transactions'))



def realizar_compra(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type):
    
    try:
        # Verificar campos obrigatórios
        redirect_result_com = check_mandatory_fields_in_purchase(payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date)
        if redirect_result_com:
            return redirect_result_com
        
        # Carteira de pagamento
        payment_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_payment_id).first()
        # Carteira de recebimento
        receiving_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_receive_id).first()

       
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
        
        saldo_pagto_tran = False

        if crypto_payment_id != crypto_fee_id:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_tran = (fee_wallet_balance.balance >= crypto_fee_quantity) and (crypto_wallet_balance.balance >= crypto_payment_quantity)
        else:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_tran = (crypto_wallet_balance.balance >= crypto_fee_quantity + crypto_payment_quantity)

        # Verifica se tem saldo da crypto da taxa
        if saldo_pagto_tran:
           
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
            flash('Saldo Insuficiente', 'alert-danger')
            return redirect(url_for('transaction.add_transactions'))
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
        return redirect(url_for('transaction.add_transactions'))

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
        return redirect(url_for('transaction.add_transactions'))
    

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
        
        # Verificar campos obrigatórios
        redirect_result_com = check_mandatory_fields_in_purchase(payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date)
        if redirect_result_com:
            return redirect_result_com
        
        # Carteira de pagamento
        payment_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_payment_id).first()
        # Carteira de recebimento
        receiving_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_receive_id).first()

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

        saldo_pagto_tran = False

        if crypto_payment_id != crypto_fee_id:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_tran = (fee_wallet_balance.balance >= crypto_fee_quantity) and (crypto_wallet_balance.balance >= crypto_payment_quantity)
        else:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_tran = ((fee_wallet_balance.balance + crypto_wallet_balance.balance) >= (crypto_fee_quantity + crypto_payment_quantity))

        # Verifica se tem saldo da crypto da taxa
        if saldo_pagto_tran:
            
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
            
            # Registrar a transação
            session.add(transaction)
            session.commit()

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
            flash('Saldo Insuficiente!', 'alert-danger')
            return redirect(url_for('transaction.add_transactions'))
                        
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
        return redirect(url_for('transaction.add_transactions'))

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
        return redirect(url_for('transaction.add_transactions'))


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
        if payment_wallet_balance and fee_wallet_balance and (payment_wallet_balance.balance >= (crypto_receive_quantity + crypto_fee_quantity)) and fee_wallet_balance.balance >= crypto_fee_quantity:
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
            flash('Saldo Insuficiente!', 'alert-danger')
            session.rollback()            
    except Exception as e:
        flash(f'Erro ao realizar transferência: {e}', 'alert-danger')
        session.rollback()
        raise


@transaction_bp.route('/transaction.delete_transaction', methods=['POST'])
def delete_transaction():
    session = create_session()

    try:
        transacao_id = request.form.get('transactions_id')
        
        if transacao_id:
            
            transaction = session.query(Transaction).filter_by(transactions_id=transacao_id).first()
                
            if transaction:
                tipo_transacao = transaction.transaction_type
                wallet_id_saida = transaction.payment_wallet_id
                wallet_id_recebimento = transaction.receiving_wallet_id
                crypto_payment_id = transaction.crypto_payment_id
                crypto_fee_id = transaction.crypto_fee_id
                crypto_receive_id = transaction.crypto_receive_id
                crypto_payment_quantity = transaction.crypto_payment_quantity
                crypto_fee_quantity = transaction.crypto_fee_quantity
                crypto_receive_quantity = transaction.crypto_receive_quantity

                balance = True

                # Busca os saldos
                wallet_balance_payment = session.query(WalletBalance).filter_by(balance_wallet_id=wallet_id_saida, balance_crypto_id=crypto_payment_id).first()
                    
                wallet_balance_fee = session.query(WalletBalance).filter_by(balance_wallet_id=wallet_id_saida, balance_crypto_id=crypto_fee_id).first()
                   
                wallet_balance_receive = session.query(WalletBalance).filter_by(balance_wallet_id=wallet_id_recebimento, balance_crypto_id=crypto_receive_id).first()    
                    
                if wallet_balance_receive:
                    if wallet_balance_receive.balance >= crypto_receive_quantity:
                        wallet_balance_receive.balance -= crypto_receive_quantity
                        session.add(wallet_balance_receive)
                            
                        if wallet_balance_payment:
                            wallet_balance_payment.balance += crypto_payment_quantity
                            session.add(wallet_balance_payment)
                            
                        if wallet_balance_fee:
                            wallet_balance_fee.balance += crypto_fee_quantity
                            if tipo_transacao == 'Transferência':
                                wallet_balance_fee.balance += crypto_receive_quantity
                                session.add(wallet_balance_fee)
                                session.add(wallet_balance_fee)                        

                        session.add(wallet_balance_receive)                        
                    else:
                        balance = False
                        flash('Saldo Insuficiente para Excluir Recebimento.', 'alert-danger') 
                        
                    if balance:
                        # Exclui a transação
                        session.delete(transaction)
                        session.commit()
                        flash(f'Transação deletada com sucesso.', 'alert-success')
                    else:
                        flash(f'Transação não tem saldo para poder ser excluida.', 'alert-danger')
        else:
            flash("Transação não encontrada.", 'alert-danger')

    except Exception as e:
        flash(f'Erro ao tentar excluir transação: {e}', 'alert-danger')
        if session:
            session.rollback()

    finally:
        session.close()

    return redirect(url_for('transaction.transactions'))


@transaction_bp.route('/add_transactions/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    session = None
    transaction = None
    
    try:
        #estou na rota que consulta o banco e mostra as trsnsaçãoes existentes, nesta página tem o botão de excluir que deve pegar nesta tabela  o id da transação

        # com id em mãos deve buscar os dados da referida transação no banco

        #abrir a página add_transactions.html que é o formulário das transações e preencher o mesmo com dados do banco conforme id

        # estando com o formulário preenchido quando usuário clicar no botão, vai chamar a função que vai deletar a transação do banco e já corrige os saldo

        #após excluir vai salvar a transação no banco com mesmo id
        pass
            
    except Exception as e:
        if session is not None:
            session.rollback()
        flash(f'Erro ao tentar atualizar a transação: {e}', 'alert-danger')

    return render_template('operacoes/edit_transaction.html', transaction=transaction)