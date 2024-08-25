from flask import render_template, url_for, flash, request, redirect,jsonify
from sqlalchemy import func, text
from criptoControl.forms import TransacaoForm, AddWalletForm, AddCryptoForm
from criptoControl.models import db, Wallet, Cryptocurrency, WalletBalance, Transaction, Price
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

    try:
        # Busca as informações no banco
        transacoes = session.query(Transaction).order_by(Transaction.id.desc()).all()
        carteiras = session.query(Wallet).filter(Wallet.status=='N').all()
        moedas = session.query(Cryptocurrency).filter(Cryptocurrency.status=='N').all()

        # Popular as informações do banco no HTML
        formTransacoes.moedaTransacao.choices = [('', '')] + [(moeda.id, f"{moeda.name}({moeda.symbol})") for moeda in moedas]
        formTransacoes.moedaTaxa.choices = [('', '')] + [(moeda.id, f"{moeda.name}({moeda.symbol})") for moeda in moedas]
        formTransacoes.carteriaSaidaTransacao.choices = [('', '')] + [(carteira.id, carteira.name) for carteira in carteiras]
        formTransacoes.carteriaRecebimentoTransacao.choices = [('', '')] + [(carteira.id, carteira.name) for carteira in carteiras]
    finally:
        session.close()
    
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
    query = text("""
    SELECT
        w.name AS carteira,
        w.network AS Rede,
        SUM(wb.balance * p.price) AS total_valor
    FROM 
        wallet_balances wb
    JOIN 
        wallets w ON w.id = wb.wallet_id
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
        AND p.timestamp = latest_price.latest_timestamp
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
                wallet = session.query(Wallet).filter_by(id=carteira_id).first()
                
                if not wallet:
                    flash(f'Carteira não encontrada.', 'alert-danger')
                    return redirect(url_for('carteiras'))

                # Verifica se há transações associadas à carteira
                trans_carteira = session.query(Transaction).filter_by(wallet_id=wallet.id).first()
                taxa_carteira = session.query(Transaction).filter_by(receiving_wallet_id=wallet.id).first()

                if not trans_carteira and not taxa_carteira:
                    # Se não há transações associadas, deleta a carteira
                    session.delete(wallet)
                    session.commit()
                    flash(f'Carteira deletada com sucesso.', 'alert-success')
                else:
                    # Se há transações associadas, atualiza o status para 'S'
                    wallet.status = 'S'
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
                trans_moeda = session.query(Transaction).filter_by(crypto_Trans_id=crypto_id).first()
                taxa_moeda = session.query(Transaction).filter_by(fee_crypto_id=crypto_id).first()
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
                
        wallet_id_recebimento = request.form.get('carteriaRecebimentoTransacao')
        wallet_id_saida = request.form.get('carteriaSaidaTransacaoId')
        crypto_trans_id = request.form.get('moedaTransacao')
        crypto_price = float(request.form.get('precoTransacao', 0))
        crypto_quantity = float(request.form.get('quantidadeTransacao', 0))
        transaction_total = float(request.form.get('totalTransacao', 0))                        
        transaction_type = request.form.get('tipoTransacao')
        date_trans = request.form.get('dataTransacao')

        
        # Cria a sessão
        with app.app_context():
            session = create_session()

            if transaction_type != 'Saldo':
                fee_crypto_id = request.form.get('moedaTaxa')
                fee_price = float(request.form.get('precoTaxa', 0))
                fee_quantity = float(request.form.get('quantidadeTaxa', 0))
                fee_total = float(request.form.get('totalTaxa', 0))

            if date_trans == '':
                date_trans = datetime.now()
            else:
                date_trans = datetime.strptime(date_trans, '%Y-%m-%d')

            # Supondo que você tenha uma função de transação definida para realizar as operações
            if transaction_type == 'Compra':
                realizar_compra(session, wallet_id_recebimento, crypto_trans_id, crypto_price, crypto_quantity, fee_crypto_id, fee_price, fee_quantity, fee_total, transaction_total,date_trans)
            elif transaction_type == 'Saldo':
                inserir_saldo(session, wallet_id_recebimento, crypto_trans_id, crypto_price, crypto_quantity, transaction_total, date_trans)
            elif transaction_type == 'Venda':
                realizar_venda(session,  wallet_id_saida, crypto_trans_id, crypto_price, crypto_quantity, fee_crypto_id, fee_price, fee_quantity, fee_total, transaction_total, date_trans)
            elif transaction_type == 'Transferência':
                realizar_transferencia(session, wallet_id_recebimento, wallet_id_saida,crypto_trans_id, crypto_quantity, crypto_price, fee_crypto_id, fee_price, fee_quantity, fee_total, transaction_total, date_trans)
        
            session.commit()
            
    except Exception as e:
        if session is not None:
            session.rollback()  # Apenas tenta fazer o rollback se a sessão foi criada
        flash(f'Erro ao tentar adicionar transação: {e}', 'alert-danger')
        print(f'Erro ao tentar adicionar transação: {e}')  # Adicionado para ajudar na depuração
    
    return redirect(url_for('transacoes'))
    

# ***************** TRANSAÇÃO DE COMPRA  ******************#

def realizar_compra(session, wallet_id_recebimento, crypto_trans_id, crypto_price, crypto_quantity, fee_crypto_id, fee_price, fee_quantity, fee_total, transaction_total, date_trans):
    
    try:
        print(f'Realizando compra de {crypto_quantity} unidades de {crypto_trans_id} a {crypto_price} cada.')

        # consulta se a moeda da transação já existe
        wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id_recebimento, cryptocurrency_id=crypto_trans_id).first()
        
        # consulta se tem saldo suficiente para a taxa 
        fee_wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id_recebimento, cryptocurrency_id=fee_crypto_id).filter(WalletBalance.balance > fee_quantity).first()

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
                    wallet_id=wallet_id_recebimento,
                    cryptocurrency_id=crypto_trans_id,
                    balance=crypto_quantity
                )
                session.add(novo_saldo)

            # Deduz a taxa
            fee_wallet_balance.balance -= fee_quantity

            # Criar a transação
            transaction = Transaction(
                wallet_id=wallet_id_recebimento,
                crypto_Trans_id=crypto_trans_id,
                crypto_price=crypto_price,
                crypto_quantity=crypto_quantity,
                transaction_total=transaction_total,
                type='Compra',
                fee_crypto_id=fee_crypto_id,
                fee_price=fee_price,
                fee_quantity=fee_quantity,
                fee_total=fee_total,
                receiving_wallet_id=wallet_id_recebimento,
                date=date_trans
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

def inserir_saldo(session, wallet_id_recebimento, crypto_trans_id, crypto_price, crypto_quantity, transaction_total, date_trans):
    try:
        sfee_price = 0.0
        sfee_quantity = 0.0
        sfee_total = 0.0
        sfee_crypto_id = ''

        print(f'Inserindo Saldo {crypto_quantity} unidades de {crypto_trans_id} a {crypto_price} cada.')

        # Obter o saldo atual da carteira para a criptomoeda específica
        wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id_recebimento, cryptocurrency_id=crypto_trans_id).first()
        
        print('Taxa zero, logo inserção de saldo')
        # Atualizar o saldo da criptomoeda após a compra
        if wallet_balance is not None:
            # Atualiza o saldo existente
            wallet_balance.balance += crypto_quantity            
        else:
            # Cria um novo registro em WalletBalance
            novo_saldo = WalletBalance(
                wallet_id=wallet_id_recebimento,
                cryptocurrency_id=crypto_trans_id,
                balance=crypto_quantity
            )
            session.add(novo_saldo)

        # Criar a transação
        transaction = Transaction(
            wallet_id=wallet_id_recebimento,
            crypto_Trans_id=crypto_trans_id,
            crypto_price=crypto_price,
            crypto_quantity=crypto_quantity,
            transaction_total=transaction_total,
            type='Saldo',
            fee_crypto_id=sfee_crypto_id,
            fee_price=sfee_price,
            fee_quantity=sfee_quantity,
            fee_total=sfee_total,
            receiving_wallet_id=wallet_id_recebimento,
            date=date_trans
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
def realizar_venda(session,  wallet_id_saida, crypto_trans_id, crypto_price, crypto_quantity, fee_crypto_id, fee_price, fee_quantity, fee_total, transaction_total, date_trans):
    
    #wallet_id_saida = request.form.get('carteriaSaidaTransacaoId')
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
                date=date_trans
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


def realizar_transferencia(session, wallet_id_recebimento, wallet_id_saida,crypto_trans_id, crypto_quantity, crypto_price, fee_crypto_id, fee_price, fee_quantity, fee_total, transaction_total, date_trans):
        
    try:
        print(f'Realizando venda de {crypto_quantity} unidades da moeda id {crypto_trans_id} a um preço de {crypto_price} cada.')

        # consulta se tem saldo para moeda transferida
        wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id_saida, cryptocurrency_id=crypto_trans_id).filter(WalletBalance.balance > crypto_quantity).first()
        
        # consulta se tem saldo suficiente para a taxa 
        fee_wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id_saida, cryptocurrency_id=fee_crypto_id).filter(WalletBalance.balance > fee_quantity).first()

        # consulta se a moeda transferida existe em balance
        wallet_balance_receb = session.query(WalletBalance).filter_by(wallet_id=wallet_id_recebimento, cryptocurrency_id=crypto_trans_id).first()

        print(f'wallet_id: {wallet_id_saida}')
        print(f'wallet_id_recebimento: {wallet_id_recebimento}')
        print(f'crypto_trans_id: {crypto_trans_id}')
        print(f'fee_crypto_id: {fee_crypto_id}')

        #verifica se tem saldo das moedas 
        if (wallet_balance is not None) and (fee_wallet_balance is not None):
            print(f'Saldo da taxa: {fee_wallet_balance.balance}')
            print(f'Saldo da moeda transferida: {wallet_balance.balance}')

            # Deduz moeda transferida
            wallet_balance.balance -= crypto_quantity 
            
            # Deduz a taxa
            fee_wallet_balance.balance -= fee_quantity 

            # adiciona a moeda transferida na carteira
            if wallet_balance_receb is not None:
                # Adiciona a moeda transferida
                wallet_balance_receb.balance += crypto_quantity 
            else:                                
                # se a moeda não existe em balance, insere
                novo_recebimento_trans = WalletBalance(
                    wallet_id=wallet_id_recebimento,
                    cryptocurrency_id=crypto_trans_id,
                    balance=crypto_quantity
                )
                session.add(novo_recebimento_trans)

            
            # Criar a transação
            transaction = Transaction(
                wallet_id=wallet_id_saida,
                crypto_Trans_id=crypto_trans_id,
                crypto_price=crypto_price,
                crypto_quantity=crypto_quantity,
                transaction_total=transaction_total,
                type='Transferência',
                fee_crypto_id=fee_crypto_id,
                fee_price=fee_price,
                fee_quantity=fee_quantity,
                fee_total=fee_total,
                receiving_wallet_id=wallet_id_recebimento,
                date=date_trans
            )

            # Registrar a transação
            session.add(transaction)

            # Força a detecção das mudanças antes do commit
            session.flush()

            # Commit das mudanças
            session.commit()
            print('Transferência realizada com sucesso.')

    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Venda: {e}', 'alert-danger')
        print(f'Erro na Transação de Venda: {e}')
        raise


@app.route('/delete_transacao', methods=['POST'])
def delete_transacao():
    session = create_session()
    print('deletar passo 1')
    try:
        # Obtém o ID da transacao a partir do formulário
        transacao_id = request.form.get('transacao_id')
        if transacao_id:
            with app.app_context():
                # Busca a carteira pelo ID
                transacao = session.query(Transaction).filter_by(id=transacao_id).first()
                print('deletar passo 2')
                if transacao:
                    # deleta transação pelo id
                    session.delete(transacao)
                    session.commit()
                    flash(f'Transação deletada com sucesso', 'alert-success')
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
            Price.cryptocurrency_id,
            func.max(Price.timestamp).label('latest_timestamp')
        )
        .group_by(Price.cryptocurrency_id)
        .subquery()
    )
    
    # Consulta principal
    query = (
        db.session.query(
            Wallet.name.label('carteira'),
            Cryptocurrency.name.label('moeda'),
            WalletBalance.balance.label('quantidade'),
            Price.price.label('preço'),
            (WalletBalance.balance * Price.price).label('valor')
        )
        .join(WalletBalance, Wallet.id == WalletBalance.wallet_id)
        .join(Cryptocurrency, Cryptocurrency.id == WalletBalance.cryptocurrency_id)
        .join(Price, Price.cryptocurrency_id == Cryptocurrency.id)
        .join(latest_prices_subquery, 
               (Price.cryptocurrency_id == latest_prices_subquery.c.cryptocurrency_id) &
               (Price.timestamp == latest_prices_subquery.c.latest_timestamp))
        .order_by(Wallet.name)
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