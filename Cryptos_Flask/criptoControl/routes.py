from flask import render_template, url_for, flash, request, redirect,jsonify
from sqlalchemy import func, text
from criptoControl.forms import TransacaoForm, AddWalletForm, AddCryptoForm
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
    formTransacoes = TransacaoForm()
    formAddCarteiras = AddWalletForm()
    formAddMoedas = AddCryptoForm()
    session = create_session()

    try:        
        # Busca as informações no banco
        cons_transactions = session.query(Transaction).all()
        cons_wallets = session.query(Wallet).filter(Wallet.wallet_status=='N').all()
        cons_crypto = session.query(Cryptocurrency).filter(Cryptocurrency.crypto_status=='N').all()       
    finally:
        session.close()    
    return render_template('index.html', cons_transactions=cons_transactions, cons_wallets=cons_wallets, cons_crypto=cons_crypto, formTransacoes=formTransacoes, formAddCarteiras=formAddCarteiras, formAddMoedas=formAddMoedas)



#***** ROTA TRANSAÇÕES *****
@app.route('/transacoes')
def transacoes():
    try:
        session = create_session()
        transacoes = Transaction.query.options(joinedload(Transaction.payment_wallet)).all()
    finally:
        session.close()
    return render_template('transactions.html', transacoes=transacoes)

@app.route('/add_transacoes')
def adicionar_transacoes(): 
    formTransacoes = TransacaoForm()
    formAddCarteiras = AddWalletForm()
    formAddMoedas = AddCryptoForm()
    session = create_session()

    try:        
        # Busca as informações no banco
        transacoes = session.query(Transaction).all()
        carteiras = session.query(Wallet).filter(Wallet.wallet_status=='N').all()
        moedas = session.query(Cryptocurrency).filter(Cryptocurrency.crypto_status=='N').all()

        # Popular as informações do banco no HTML
        formTransacoes.crypto_payment.choices = [('', '')] + [(moeda.crypto_id, f"{moeda.name}({moeda.symbol})") for moeda in moedas]
        
        formTransacoes.crypto_fee.choices = [('', '')] + [(moeda.crypto_id, f"{moeda.name}({moeda.symbol})") for moeda in moedas]

        formTransacoes.crypto_receive.choices = [('', '')] + [(moeda.crypto_id, f"{moeda.name}({moeda.symbol})") for moeda in moedas]

        formTransacoes.payment_wallet.choices = [('', '')] + [(carteira.wallet_id, carteira.name) for carteira in carteiras]
        
        formTransacoes.receiving_wallet.choices = [('', '')] + [(carteira.id, carteira.name) for carteira in carteiras]
    finally:
        session.close()
    
    return render_template('add_transactions.html', transacoes=transacoes, carteiras=carteiras, moedas=moedas, formTransacoes=formTransacoes, formAddCarteiras=formAddCarteiras, formAddMoedas=formAddMoedas)


#***** ROTA PREÇOS *****
@app.route('/precos')
def precos():
    with app.app_context():
        session = create_session()
        
        # Subconsulta para obter o preço mais recente de cada criptomoeda
        subquery = (
            session.query(Price.price_crypto_id, func.max(Price.price_consult_datetime).label('latest_timestamp'))
            .group_by(Price.price_crypto_id)
            .subquery()
        )
        
        # Consulta principal para obter os preços mais recentes
        precos = (
            session.query(Price)
            .join(subquery, (Price.price_crypto_id == subquery.c.price_crypto_id) &
                                (Price.price_consult_datetime == subquery.c.latest_timestamp))
            .join(Cryptocurrency, Price.price_crypto_id == Cryptocurrency.crypto_id)
            .filter(Cryptocurrency.crypto_id == 'N')
            .all()
        )
    
    return render_template('prices.html', precos=precos)



#***** ROTA CARTEIRAS *****
@app.route('/carteiras')
def carteiras():
    '''query = text("""
        SELECT
            w.name AS carteira,
            w.network AS Rede,
            SUM(wb.balance * p.price) AS total_valor
        FROM 
            wallet_balances wb
        JOIN 
            wallets w ON w.id = wb.payment_wallet_id
        JOIN 
            cryptocurrencies c ON c.id = wb.cryptocurrency_id
        JOIN 
            prices p ON p.cryptocurrency_id = c.id
        JOIN 
            (
                SELECT 
                    cryptocurrency_id, 
                    MAX(timestamp) AS latest_timestamp 
                FROM 
                    prices 
                GROUP BY 
                    cryptocurrency_id
            ) latest_price 
            ON p.cryptocurrency_id = latest_price.cryptocurrency_id 
            AND pconsultation_datetime = latest_price.latest_timestamp
        WHERE 
            w.status <> 'S'
        GROUP BY 
            w.name, w.network
        ORDER BY 
            w.name;
        """)
    
    with app.app_context():
        result = db.session.execute(query)
        carteiras = result.fetchall()
        print(carteiras) '''
    
    with app.app_context():
        carteiras = Wallet.query.filter(Wallet.wallet_status != 'S').order_by(Wallet.wallet_name).all()
    
    return render_template('wallets.html', carteiras=carteiras)


#***** ROTA MOEDAS *****
@app.route('/moedas')
def moedas():
    with app.app_context():
        moedas = Cryptocurrency.query.filter(Cryptocurrency.crypto_status != 'S').order_by(Cryptocurrency.crypto_name).all()
    return render_template('cryptos.html', moedas=moedas)

#----------------------  FIM ROTAS-------------------------
#****************************************************************
#----------------------  ATIVIDADE ROTA ADICIONAR TRANSAÇÃO-------------------------
#Pega preço atual da morda para preencher campos tela transsação
@app.route('/get_price/<int:cryptocurrency_id>', methods=['GET'])
def get_price(cryptocurrency_id):
    session = create_session()    
    # Busca o preço mais recente da moeda selecionada
    latest_price = session.query(Price.price).filter(Price.price_crypto_id == cryptocurrency_id).order_by(Price.price_consultation_datetime.desc()).first()
    
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
            wallet_name = formAddCarteiras.wallet_name.data.upper()
            wallet_network = formAddCarteiras.wallet_network.data.upper()
            with app.app_context():
                carteira = Wallet(user_id=1, name=wallet_name, network=wallet_network) #???remover user_id
                session.add(carteira)
                session.commit()
                flash(f'A carteira {(formAddCarteiras.wallet_name.data).upper()} foi adicionada com sucesso', 'alert-success')
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
        carteira_id = request.form.get('payment_wallet_id')
        if carteira_id:
            with app.app_context():
                # Busca a carteira pelo ID
                payment_wallet = session.query(Wallet).filter_by(wallet_id=carteira_id).first()
                
                if not payment_wallet:
                    flash(f'Carteira não encontrada.', 'alert-danger')
                    return redirect(url_for('carteiras'))

                # Verifica se há transações associadas à carteira
                trans_carteira = session.query(Transaction).filter_by(payment_wallet_id=payment_wallet.transactions_id).first()
                taxa_carteira = session.query(Transaction).filter_by(receiving_wallet_id=payment_wallet.transactions_id).first()

                if not trans_carteira and not taxa_carteira:
                    # Se não há transações associadas, deleta a carteira
                    session.delete(payment_wallet)
                    session.commit()
                    flash(f'Carteira deletada com sucesso.', 'alert-success')
                else:
                    # Se há transações associadas, atualiza o status para 'S'
                    payment_wallet.status = 'S'
                    session.commit()
                    flash(f'Carteira desativada pois já tiveram transações com ela.', 'alert-success')
        else:
            flash("ID da carteira não fornecido", 'alert-danger')
    except Exception as e:
        flash(f'Erro ao tentar desativar a carteira: {e}', 'alert-danger')
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
            cripto_name = formAddMoedas.crypto_name.data.upper()
            cripto_symbol = formAddMoedas.crypto_symbol.data.upper()
            with app.app_context():
                moeda = Cryptocurrency(name=cripto_name, symbol=cripto_symbol)
                session.add(moeda)
                session.commit()
                flash(f'A moeda {(formAddMoedas.crypto_name.data).upper()} foi adicionada com sucesso', 'alert-success')
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
                moeda = session.query(Cryptocurrency).filter_by(crypto_id=crypto_id).first()
                trans_moeda = session.query(Transaction).filter_by(crypto_payment_id=crypto_id).first()
                taxa_moeda = session.query(Transaction).filter_by(crypto_fee_id=crypto_id).first()
                if moeda and not trans_moeda and not taxa_moeda:
                    session.delete(moeda)
                    session.commit()
                    flash(f'Moeda deletada com sucesso.', 'alert-success')
                else:
                    # Atualiza o campo de status para 'S'
                    moeda.status = 'S'
                    session.commit()
                    flash(f'Moeda apenas desativada, pois tiveram transações com ela.', 'alert-success')
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
            crypto_payment_price = Price(cryptocurrency_id=crypto_id, price=price, timestamp=timestamp)
            session.add(crypto_payment_price)
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
                price = get_crypto_payment_price(COINMARKETCAP_API_KEY, crypto.symbol)
                if price is not None:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    crypto_payment_price = Price(crypto_id=crypto.id, price=price, timestamp=timestamp)
                    session.add(crypto_payment_price)
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
                
        wallet_id_recebimento = request.form.get('receiving_wallet')
        wallet_id_saida = request.form.get('payment_wallet')
        crypto_payment_id = request.form.get('crypto_payment')
        crypto_payment_price = float(request.form.get('crypto_payment_price', 0))
        crypto_payment_quantity = float(request.form.get('crypto_payment_quantity', 0))
        total_paid = float(request.form.get('total_paid', 0))                        
        type = request.form.get('transaction_type')
        date_trans = request.form.get('transaction_date')
        crypto_receive_id = request.form.get('crypto_receive')
        crypto_receive_price = float(request.form.get('crypto_receive_price', 0))
        crypto_receive_quantity = float(request.form.get('crypto_receive_quantity', 0))
              
        # Cria a sessão
        with app.app_context():
            session = create_session()

            if type != 'Saldo':
                crypto_fee_id = request.form.get('crypto_fee')
                crypto_fee_price = float(request.form.get('crypto_fee_price', 0))
                crypto_fee_quantity = float(request.form.get('crypto_fee_quantity', 0))
                total_fee = float(request.form.get('total_fee', 0))

            if date_trans == '':
                date_trans = datetime.now()
            else:
                date_trans = datetime.strptime(date_trans, '%Y-%m-%d')

            # Supondo que você tenha uma função de transação definida para realizar as operações
            if type == 'Compra':
                realizar_compra(session, wallet_id_recebimento, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, total_paid,date_trans, crypto_receive_id, crypto_receive_price, crypto_receive_quantity)
            elif type == 'Saldo':
                inserir_saldo(session, wallet_id_recebimento, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, date_trans)
            elif type == 'Venda':
                realizar_venda(session,  wallet_id_saida, wallet_id_recebimento, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, total_paid, date_trans, crypto_receive_id, crypto_receive_price, crypto_receive_quantity)
            elif type == 'Transferência':
                realizar_transferencia(session, wallet_id_recebimento, wallet_id_saida,crypto_payment_id, crypto_payment_quantity, crypto_payment_price, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, total_paid, date_trans)
        
            session.commit()
            
    except Exception as e:
        if session is not None:
            session.rollback()  # Apenas tenta fazer o rollback se a sessão foi criada
        flash(f'Erro ao tentar adicionar transação: {e}', 'alert-danger')
        print(f'Erro ao tentar adicionar transação: {e}')  # Adicionado para ajudar na depuração
    
    return redirect(url_for('transacoes'))
    

# ***************** TRANSAÇÃO DE COMPRA  ******************#

def realizar_compra(session, wallet_id_recebimento, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, total_paid, date_trans, crypto_receive_id, crypto_receive_price, crypto_receive_quantity):
    
    try:
        print(f'Realizando compra de {crypto_payment_quantity} unidades de {crypto_payment_id} a {crypto_payment_price} cada.')

        # consulta se a moeda da transação já existe
        wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_recebimento, cryptocurrency_id=crypto_payment_id).first()
        
        # consulta se tem saldo suficiente para a taxa 
        fee_wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_recebimento, cryptocurrency_id=crypto_fee_id).filter(WalletBalance.balance > crypto_fee_quantity).first()

        #verifica se tem saldo da moeda da taxa 
        if fee_wallet_balance is not None:
            print(f'Saldo da taxa: {fee_wallet_balance.balance}')
            print(f'Saldo suficiente para a taxa. Deduzindo {crypto_fee_quantity} da carteira de taxa.')

            # Criar a transação
            transaction = Transaction(
                payment_wallet_id=wallet_id_recebimento,
                crypto_payment_id=crypto_payment_id,
                crypto_payment_price=crypto_payment_price,
                crypto_payment_quantity=crypto_payment_quantity,
                total_paid=total_paid,
                type='Compra',
                crypto_fee_id=crypto_fee_id,
                crypto_fee_price=crypto_fee_price,
                crypto_fee_quantity=crypto_fee_quantity,
                total_fee=total_fee,
                receiving_wallet_id=wallet_id_recebimento,
                date=date_trans,
                crypto_receive_id=crypto_receive_id,
                crypto_receive_price=crypto_receive_id,
                crypto_receive_quantity=crypto_receive_id
            )

            # Registrar a transação
            session.add(transaction)
            session.commit()

            
            if wallet_balance is not None:
                # se a moeda já existe em balance, soma
                wallet_balance.balance += crypto_payment_quantity
            else:
                # se a moeda não existe em balance, insere
                novo_saldo = WalletBalance(
                    payment_wallet_id=wallet_id_recebimento,
                    cryptocurrency_id=crypto_payment_id,
                    balance=crypto_payment_quantity
                )
                session.add(novo_saldo)

            # Deduz a taxa
            fee_wallet_balance.balance -= crypto_fee_quantity

            print('Compra realizada com sucesso.')

    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Compra: {e}', 'alert-danger')
        print(f'Erro na Transação de Compra: {e}')
        raise

#************************************************************************************************

def inserir_saldo(session, wallet_id_recebimento, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, date_trans):
    try:
        sfee_price = 0.0
        sfee_quantity = 0.0
        stotal_fee = 0.0
        sfee_crypto_id = ''

        print(f'Inserindo Saldo {crypto_payment_quantity} unidades de {crypto_payment_id} a {crypto_payment_price} cada.')

        # Obter o saldo atual da carteira para a criptomoeda específica
        wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_recebimento, cryptocurrency_id=crypto_payment_id).first()
        
        print('Taxa zero, logo inserção de saldo')

        # Criar a transação
        transaction = Transaction(
            payment_wallet_id=wallet_id_recebimento,
            crypto_payment_id=crypto_payment_id,
            crypto_payment_price=crypto_payment_price,
            crypto_payment_quantity=crypto_payment_quantity,
            total_paid=total_paid,
            type='Saldo',
            crypto_fee_id=sfee_crypto_id,
            crypto_fee_price=sfee_price,
            crypto_fee_quantity=sfee_quantity,
            total_fee=stotal_fee,
            receiving_wallet_id=wallet_id_recebimento,
            date=date_trans
        )

        session.add(transaction)
        session.commit()

        # Atualizar o saldo da criptomoeda após a compra
        if wallet_balance is not None:
            # Atualiza o saldo existente
            wallet_balance.balance += crypto_payment_quantity            
        else:
            # Cria um novo registro em WalletBalance
            novo_saldo = WalletBalance(
                payment_wallet_id=wallet_id_recebimento,
                cryptocurrency_id=crypto_payment_id,
                balance=crypto_payment_quantity
            )
            session.add(novo_saldo)
        print('Compra realizada com sucesso.')

    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Compra: {e}', 'alert-danger')
        print(f'Erro na Transação de Compra: {e}')
        raise

#************************************************************************************************
def realizar_venda(session, wallet_id_saida, wallet_id_recebimento, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, total_paid, date_trans, crypto_receive_id, crypto_receive_price, crypto_receive_quantity):
    
    # wallet_id_saida = request.form.get('payment_wallet')
    crypto_fee_id = request.form.get('crypto_fee')
    crypto_fee_price = float(request.form.get('crypto_fee_price', 0))
    crypto_fee_quantity = float(request.form.get('crypto_fee_quantity', 0))
    total_fee = float(request.form.get('total_fee', 0))

    try:
        print(f'Realizando venda de {crypto_payment_quantity} unidades da moeda id {crypto_payment_id} a um preço de {crypto_payment_price} cada.')

        if crypto_fee_id != crypto_payment_id:
            # consulta se tem saldo para moeda vendida
            wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_payment_id).filter(WalletBalance.balance >= crypto_payment_quantity).first()
            
            # consulta se tem saldo suficiente para a taxa 
            fee_wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_fee_id).filter(WalletBalance.balance >= crypto_fee_quantity).first()
        else:
            # consulta se tem saldo para moeda vendida
            wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_payment_id).filter(WalletBalance.balance >= (crypto_payment_quantity + crypto_fee_quantity)).first()
            
            # consulta se tem saldo suficiente para a taxa 
            fee_wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_fee_id).filter(WalletBalance.balance >= (crypto_fee_quantity + crypto_payment_quantity)).first()

        print(f'payment_wallet_id: {wallet_id_saida}')
        print(f'crypto_payment_id: {crypto_payment_id}')
        print(f'crypto_fee_id: {crypto_fee_id}')

        # Verifica se tem saldo das moedas 
        if (wallet_balance is not None) and (fee_wallet_balance is not None):
            print(f'Saldo da taxa: {fee_wallet_balance.balance}')
            print(f'Saldo da moeda vendida: {wallet_balance.balance}')

            # Deduz moeda vendida
            wallet_balance.balance -= crypto_payment_quantity 
            
            # Deduz a taxa
            fee_wallet_balance.balance -= crypto_fee_quantity 

            # Atualiza o saldo na carteira de recebimento
            wallet_balance_receive = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_recebimento, cryptocurrency_id=crypto_payment_id).first()

            if wallet_balance_receive:
                # Se já existe saldo, atualiza
                wallet_balance_receive.balance += crypto_payment_quantity
            else:
                # Se não existe, cria um novo registro
                novo_saldo = WalletBalance(
                    payment_wallet_id=wallet_id_recebimento,
                    cryptocurrency_id=crypto_payment_id,
                    balance=crypto_payment_quantity
                )
                session.add(novo_saldo)

            # Criar a transação
            transaction = Transaction(
                payment_wallet_id=wallet_id_saida,
                crypto_payment_id=crypto_payment_id,
                crypto_payment_price=crypto_payment_price,
                crypto_payment_quantity=crypto_payment_quantity,
                total_paid=total_paid,
                type='Venda',
                crypto_fee_id=crypto_fee_id,
                crypto_fee_price=crypto_fee_price,
                crypto_fee_quantity=crypto_fee_quantity,
                total_fee=total_fee,
                date=date_trans,
                receiving_wallet_id=wallet_id_recebimento,
                crypto_receive_id=crypto_receive_id,
                crypto_receive_price=crypto_receive_id,
                crypto_receive_quantity=crypto_receive_id
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



def realizar_transferencia(session, wallet_id_recebimento, wallet_id_saida, crypto_payment_id, crypto_payment_quantity, crypto_payment_price, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, total_paid, date_trans):
    try:
        print(f'Realizando venda de {crypto_payment_quantity} unidades da moeda id {crypto_payment_id} a um preço de {crypto_payment_price} cada.')

        if crypto_fee_id != crypto_payment_id:
            # Verifica se tem saldo para a moeda transferida
            wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_payment_id).filter(WalletBalance.balance >= crypto_payment_quantity).first()
            
            # Verifica se tem saldo suficiente para a taxa
            fee_wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_fee_id).filter(WalletBalance.balance >= crypto_fee_quantity).first()
        else:
            # Verifica se tem saldo para a moeda transferida
            wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_payment_id).filter(WalletBalance.balance >= (crypto_payment_quantity + crypto_fee_quantity)).first()
            
            # Verifica se tem saldo suficiente para a taxa
            fee_wallet_balance = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_fee_id).filter(WalletBalance.balance >= (crypto_fee_quantity + crypto_payment_quantity)).first()

        # Verifica se a moeda transferida existe em balance
        wallet_balance_receb = session.query(WalletBalance).filter_by(payment_wallet_id=wallet_id_recebimento, cryptocurrency_id=crypto_payment_id).first()

        print(f'payment_wallet_id: {wallet_id_saida}')
        print(f'wallet_id_recebimento: {wallet_id_recebimento}')
        print(f'crypto_payment_id: {crypto_payment_id}')
        print(f'crypto_fee_id: {crypto_fee_id}')

        # Verifica se há saldo suficiente das moedas
        if (wallet_balance is not None) and (fee_wallet_balance is not None):
            print(f'Saldo da taxa: {fee_wallet_balance.balance}')
            print(f'Saldo da moeda transferida: {wallet_balance.balance}')

            # Deduz a moeda transferida
            wallet_balance.balance -= crypto_payment_quantity 
            
            # Deduz a taxa
            fee_wallet_balance.balance -= crypto_fee_quantity 

            # Criar a transação
            transaction = Transaction(
                payment_wallet_id=wallet_id_saida,
                crypto_payment_id=crypto_payment_id,
                crypto_payment_price=crypto_payment_price,
                crypto_payment_quantity=crypto_payment_quantity,
                total_paid=total_paid,
                type='Transferência',
                crypto_fee_id=crypto_fee_id,
                crypto_fee_price=crypto_fee_price,
                crypto_fee_quantity=crypto_fee_quantity,
                total_fee=total_fee,
                receiving_wallet_id=wallet_id_recebimento,
                date=date_trans
            )

            # Registrar a transação
            session.add(transaction)

            # Adiciona a moeda transferida na carteira de recebimento
            if wallet_balance_receb is not None:
                wallet_balance_receb.balance += crypto_payment_quantity 
            else:                                
                # Se a moeda não existe em balance, insere
                novo_recebimento_trans = WalletBalance(
                    payment_wallet_id=wallet_id_recebimento,
                    cryptocurrency_id=crypto_payment_id,
                    balance=crypto_payment_quantity
                )
                session.add(novo_recebimento_trans)

            # Commit das mudanças
            session.commit()
            print('Transferência realizada com sucesso.')
            return True  # Indica sucesso
        else:
            print('Saldo insuficiente para realizar a transferência.')
            return False  # Indica falha devido a saldo insuficiente
    except Exception as e:
        print(f'Erro ao realizar transferência: {e}')
        session.rollback()
        return False  # Indica falha devido a exceção



@app.route('/delete_transacao', methods=['POST'])
def delete_transacao():
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
                        # Verifica se tem saldo para a moeda transferida
                        wallet_balance = session.query(WalletBalance).filter_by(
                            payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_payment_id
                        ).filter(WalletBalance.balance >= crypto_payment_quantity).first()
                        
                        # Verifica se tem saldo suficiente para a taxa
                        if transacao.transaction_type != 'Saldo':
                            fee_wallet_balance = session.query(WalletBalance).filter_by(
                                payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_fee_id
                            ).filter(WalletBalance.balance >= crypto_fee_quantity).first()
                    else:
                        # Verifica se tem saldo para a moeda transferida junto com a taxa
                        wallet_balance = session.query(WalletBalance).filter_by(
                            payment_wallet_id=wallet_id_saida, cryptocurrency_id=crypto_payment_id
                        ).filter(WalletBalance.balance >= (crypto_payment_quantity + crypto_fee_quantity)).first()
                        
                        if transacao.transaction_type != 'Saldo':
                            fee_wallet_balance = wallet_balance

                    # Busca o saldo da carteira de recebimento para venda
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
                            wallet_balance.balance -= crypto_payment_quantity 

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
    return redirect(url_for('transacoes'))










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
            Cryptocurrency.crypto_name.label('moeda'),
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
        'moeda': row.moeda,
        'quantidade': row.quantidade,
        'preço': row.preço,
        'valor': row.valor
    } for row in query], total_valor