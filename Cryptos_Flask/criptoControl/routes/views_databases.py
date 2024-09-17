from flask import Blueprint, render_template, url_for, flash, request, redirect, jsonify, session, send_file
from sqlalchemy import func, or_
from criptoControl.forms import TransactionsForm, AddWalletForm, AddCryptoForm,Users
from criptoControl.models import db, Wallet, Cryptocurrency, WalletBalance, Transaction, Price, User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, login_required
from criptoControl.api import get_crypto_payment_price
from criptoControl import app
from datetime import datetime
from sqlalchemy.orm import sessionmaker, joinedload
from decimal import Decimal, ROUND_HALF_UP
import io
import matplotlib.pyplot as plt
import logging
import email_validator


views_db_bp = Blueprint('views', __name__)
logging.basicConfig(level=logging.DEBUG)

def create_session():
    return sessionmaker(bind=db.engine)()


@views_db_bp.route('/prices')
@login_required
def prices():
    try:
        # Crie a sessão e use o contexto 'with' para garantir que a sessão seja fechada corretamente
        with create_session() as session:
            # Subconsulta para obter o preço mais recente de cada criptomoeda
            subquery = (
                session.query(Price.price_crypto_id, func.max(Price.price_consult_datetime).label('latest_timestamp'))
                .group_by(Price.price_crypto_id)
                .subquery()
            )
            
            # Consulta principal para obter os preços mais recentes
            prices = (
                session.query(Price)
                .options(joinedload(Price.price_cryptocurrency))  # Carrega dados relacionados
                .join(subquery, (Price.price_crypto_id == subquery.c.price_crypto_id) &
                                (Price.price_consult_datetime == subquery.c.latest_timestamp))
                .join(Cryptocurrency, Price.price_crypto_id == Cryptocurrency.crypto_id)
                .filter(Cryptocurrency.crypto_status == 'N')
                .order_by(Cryptocurrency.crypto_symbol)
                .all()
            )
    except Exception as e:
        # Log ou trate o erro conforme necessário
        flash(f"An error occurred: {e}")
        prices = []

    return render_template('views_databases/prices.html', prices=prices)



#***** ROTA CARTEIRAS *****
@views_db_bp.route('/wallets', endpoint='wallets')
@login_required
def wallets():
    session = None
    try:
        session = create_session()
        wallets = session.query(Wallet).filter(
            Wallet.wallet_status != 'S',
            Wallet.wallet_user_id == current_user.user_id).order_by(Wallet.wallet_name).all()
    
    finally:
        if session:
            session.close()
    
    return render_template('operacoes/wallets.html', wallets=wallets)


#***** ROTA MOEDAS *****
@views_db_bp.route('/cryptos')
@login_required
def cryptos():
    session = None
    try:
        session = create_session()
        cryptos = session.query(Cryptocurrency).filter(Cryptocurrency.crypto_status != 'S').order_by(Cryptocurrency.crypto_name).all()
    finally:
        if session:
            session.close()
    
    return render_template('operacoes/cryptos.html', cryptos=cryptos)


@views_db_bp.route('/balance_wallet')
@login_required
def balance_wallet():
    # Subconsulta para obter o preço mais recente
    latest_prices_subquery = (
        db.session.query(
            Price.price_crypto_id,
            func.max(Price.price_consult_datetime).label('latest_timestamp')
        )
        .group_by(Price.price_crypto_id)
        .subquery()
    )

    # Consulta para mostrar apenas saldo em dólares
    query_dolar = (
        db.session.query(
            Wallet.wallet_name.label('carteira'),
            func.sum(WalletBalance.balance).label('quantidade_total'),
            func.sum(WalletBalance.balance * Price.price).label('valor_total')
        )
        .join(WalletBalance, Wallet.wallet_id == WalletBalance.balance_wallet_id)
        .join(Cryptocurrency, Cryptocurrency.crypto_id == WalletBalance.balance_crypto_id)
        .join(Price, Price.price_crypto_id == Cryptocurrency.crypto_id)
        .join(User, User.user_id == Wallet.wallet_user_id)
        .join(latest_prices_subquery, 
               (Price.price_crypto_id == latest_prices_subquery.c.price_crypto_id) &
               (Price.price_consult_datetime == latest_prices_subquery.c.latest_timestamp))
        .filter(WalletBalance.balance > 0)
        .filter(~Cryptocurrency.crypto_symbol.like('%BRL%'))  # Excluir 'BRL'
        .filter(User.user_id == current_user.user_id)
        .group_by(Wallet.wallet_name)
        .order_by(Wallet.wallet_name)
        .all()
    )

    # Consulta para mostrar apenas saldo em reais
    query_real = (
        db.session.query(
            Wallet.wallet_name.label('carteira'),
            func.sum(WalletBalance.balance).label('quantidade_total'),
            func.sum(WalletBalance.balance * Price.price).label('valor_total')
        )
        .join(WalletBalance, Wallet.wallet_id == WalletBalance.balance_wallet_id)
        .join(Cryptocurrency, Cryptocurrency.crypto_id == WalletBalance.balance_crypto_id)
        .join(Price, Price.price_crypto_id == Cryptocurrency.crypto_id)
        .join(User, User.user_id == Wallet.wallet_user_id)
        .join(latest_prices_subquery, 
               (Price.price_crypto_id == latest_prices_subquery.c.price_crypto_id) &
               (Price.price_consult_datetime == latest_prices_subquery.c.latest_timestamp))
        .filter(WalletBalance.balance > 0)
        .filter(Cryptocurrency.crypto_symbol.like('%BRL%'))  # Apenas 'BRL'
        .filter(User.user_id == current_user.user_id)
        .group_by(Wallet.wallet_name)
        .order_by(Wallet.wallet_name)
        .all()
    )
    
    # Calcular a soma total dos valores de todas as carteiras em dólar e real
    total_valor_dolar = sum(row.valor_total for row in query_dolar)
    total_valor_real = sum(row.valor_total for row in query_real)
    
    # Preparar os dados para renderização
    results_dolar = [{
        'carteira': row.carteira,
        'quantidade_total': row.quantidade_total,
        'valor_total': row.valor_total
    } for row in query_dolar]

    results_real = [{
        'carteira': row.carteira,
        'quantidade_total': row.quantidade_total,
        'valor_total': row.valor_total
    } for row in query_real]
    
    # Renderiza o template com os dados necessários
    return render_template('views_databases/wallet_balance.html', carteiras_dolar=results_dolar, total_valor_dolar=total_valor_dolar, carteiras_real=results_real, total_valor_real=total_valor_real)


@views_db_bp.route('/lucro_prejuizo')
@login_required
def lucro_prejuizo():
    # Subconsulta para obter o preço mais recente de cada criptomoeda
    latest_prices_subquery = (
        db.session.query(
            Price.price_crypto_id,
            func.max(Price.price_consult_datetime).label('latest_timestamp')
        )
        .group_by(Price.price_crypto_id)
        .subquery()
    )

    # Consulta para calcular o DCA (Preço Médio de Compra)
    dca_cte = (
        db.session.query(
            Wallet.wallet_id,
            Cryptocurrency.crypto_id,
            (func.sum(Transaction.crypto_receive_quantity * Transaction.crypto_receive_price) /
             func.sum(Transaction.crypto_receive_quantity)).label('dca')
        )
        .join(Wallet, Transaction.receiving_wallet_id == Wallet.wallet_id)
        .join(Cryptocurrency, Transaction.crypto_receive_id == Cryptocurrency.crypto_id)
        .filter(Transaction.transaction_type == 'Compra')
        .filter(Transaction.crypto_receive_quantity > 0)
        .group_by(Wallet.wallet_id, Cryptocurrency.crypto_id)
        .cte('dca_cte')
    )

    # Consulta para mostrar o Lucro/Prejuízo
    lucro_prejuizo_query = (
        db.session.query(
            Wallet.wallet_name.label('Carteira'),
            Cryptocurrency.crypto_symbol.label('Moeda'),
            func.strftime('%d/%m/%Y', Transaction.transaction_date).label('Data Venda'),
            Transaction.crypto_payment_quantity.label('Quantidade Vendida'),
            Transaction.crypto_payment_price.label('Preço de Venda'),
            dca_cte.c.dca.label('DCA (Preço Médio de Compra)'),
            ((Transaction.crypto_payment_price - dca_cte.c.dca) * Transaction.crypto_payment_quantity).label('Lucro/Prejuízo')
        )
        .join(Wallet, Transaction.payment_wallet_id == Wallet.wallet_id)
        .join(Cryptocurrency, Transaction.crypto_payment_id == Cryptocurrency.crypto_id)
        .outerjoin(dca_cte, (dca_cte.c.wallet_id == Wallet.wallet_id) & (dca_cte.c.crypto_id == Cryptocurrency.crypto_id))
        .filter(Transaction.transaction_type == 'Venda')
        .filter(Transaction.crypto_payment_quantity > 0)
        .filter(Wallet.wallet_user_id == current_user.user_id)
        .order_by(Transaction.transaction_date)
        .all()
    )

    # Preparando os dados para o template, usando índices para acessar os itens da tupla
    lucro_prejuizo_data = [
        {
            'Carteira': row[0],  # Wallet.wallet_name
            'Moeda': row[1],     # Cryptocurrency.crypto_symbol
            'Data Venda': row[2], # Transaction.transaction_date
            'Quantidade Vendida': row[3],  # Transaction.crypto_payment_quantity
            'Preço de Venda': row[4],  # Transaction.crypto_payment_price
            'DCA (Preço Médio de Compra)': row[5],  # dca_cte.c.dca
            'Lucro/Prejuízo': row[6]  # Lucro/Prejuízo
        }
        for row in lucro_prejuizo_query
    ]

    # Calcula o total de Lucro/Prejuízo
    total_lucro_prejuizo = sum(row['Lucro/Prejuízo'] for row in lucro_prejuizo_data)

    # Define se o resultado final é lucro ou prejuízo
    resultado_final = 'Lucro' if total_lucro_prejuizo > 0 else 'Prejuízo'

    # Renderiza o template com os dados
    return render_template('views_databases/crypto_lucroXprejuizo.html', 
                           lucro_prejuizo_data=lucro_prejuizo_data, 
                           total_lucro_prejuizo=total_lucro_prejuizo, 
                           resultado_final=resultado_final)


@views_db_bp.route('/dca_compras')
@login_required
def dca_compras():
    # Consulta SQL para calcular o DCA (Preço Médio de Compra) por carteira e moeda
    dca_query = (
        db.session.query(
            Wallet.wallet_name.label('Carteira'),
            Cryptocurrency.crypto_symbol.label('Moeda'),
            (func.sum(Transaction.crypto_receive_quantity * Transaction.crypto_receive_price) /
             func.sum(Transaction.crypto_receive_quantity)).label('DCA')
        )
        .join(Wallet, Transaction.receiving_wallet_id == Wallet.wallet_id)
        .join(User, Wallet.wallet_user_id == User.user_id)
        .join(Cryptocurrency, Transaction.crypto_receive_id == Cryptocurrency.crypto_id)
        .filter(or_(
            Transaction.transaction_type == 'Compra',
            Transaction.transaction_type == 'Saldo'
        ))
        .filter(User.user_id == current_user.user_id)  # Usuário logado
        .group_by(Cryptocurrency.crypto_symbol, Wallet.wallet_name)
        .all()
    )

    # Preparando os dados para o template
    dca_compras_data = [
        {
            'Carteira': row[0],  # Nome da Carteira
            'Moeda': row[1],     # Símbolo da Moeda
            'DCA': row[2]        # Preço Médio de Compra
        }
        for row in dca_query
    ]

    # Renderiza o template com os dados
    return render_template('views_databases/crypto_DCA.html', dca_compras_data=dca_compras_data)


# ************ MOSTRAR SALDOS DE MOEDA POR CARTERIA ****************
@views_db_bp.route('/wallet_summary')
def wallet_summary():
    # Obtém os dados de todas as carteiras
    vw_saldos, total_valor = get_wallet_summary()
    
    # Renderiza o template passando os dados
    return render_template('views_databases/wallet_summary.html', saldos=vw_saldos, total_valor=total_valor)


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
        .join(Price, Price.price_crypto_id == Cryptocurrency.crypto_id)
        .join(User, User.user_id == Wallet.wallet_user_id)
        .join(latest_prices_subquery, 
               (Price.price_crypto_id == latest_prices_subquery.c.price_crypto_id) &
               (Price.price_consult_datetime == latest_prices_subquery.c.latest_timestamp))
        .filter(WalletBalance.balance > 0)
        .filter(User.user_id == current_user.user_id)
        .order_by(Wallet.wallet_name, Cryptocurrency.crypto_name)
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