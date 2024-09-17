from flask import Blueprint, render_template, url_for, flash, request, redirect, jsonify, session, send_file
from sqlalchemy import func, or_
from criptoControl.forms import TransactionsForm, AddWalletForm, AddCryptoForm,Users
from criptoControl.models import db, Wallet, Cryptocurrency, WalletBalance, Transaction, Price, User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, login_required
from criptoControl.api import get_crypto_payment_price
from datetime import datetime
from sqlalchemy.orm import sessionmaker, joinedload
from decimal import Decimal, ROUND_HALF_UP
import io
import matplotlib.pyplot as plt
import logging
import email_validator


update_price_bp = Blueprint('update_price', __name__)

logging.basicConfig(level=logging.DEBUG)

def create_session():
    return sessionmaker(bind=db.engine)()


# VER PARA ADICIONAR PREÇO MANUALMENTE!!!!!!!!!!!???????????????????????
@update_price_bp.route('/add_price', methods=['POST'])
def add_price():
    session = None
    try:
        crypto_id = request.form['cryptocurrency_id']
        price = float(request.form['price'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session = create_session()
        crypto_payment_price = Price(cryptocurrency_id=crypto_id, price=price,timestamp=timestamp)
        session.add(crypto_payment_price)
        session.commit()
    except Exception as e:
        if session:
            session.rollback()
        flash(f'Erro ao tentar atualizar os preços: {e}', 'alert-danger')
    
    finally:
        if session:
            session.close()
    
    return redirect(url_for('views.prices'))


#Atualiza os preços das cryptos cadastradas pela API
@update_price_bp.route('/update_prices', methods=['POST'])
def update_prices():
    session = None
    try:
        COINMARKETCAP_API_KEY = '122d6732-65df-475c-8f1d-d7a95ab45bc5'
        session = create_session()
            
        # Obter todos os símbolos das criptomoedas com status 'N'
        cryptos = session.query(Cryptocurrency).filter_by(crypto_status='N').all()
        symbols = [crypto.crypto_symbol for crypto in cryptos if crypto.crypto_symbol.isalnum()]
            
        # Consultar a API uma vez para todos os símbolos
        prices = get_crypto_payment_price(COINMARKETCAP_API_KEY, symbols)
            
        # Atualizar o banco de dados com os preços obtidos
        for crypto in cryptos:
            symbol = crypto.crypto_symbol
            if symbol in prices:
                price = prices[symbol]
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                crypto_price = Price(price_crypto_id=crypto.crypto_id, price=price,price_consult_datetime=timestamp)
                session.add(crypto_price)
                flash(f'Preço da criptomoeda {symbol} atualizado com sucesso', 'alert-success')
            else:
                flash(f'Preço para a criptomoeda {symbol} não encontrado', 'alert-warning')
            
        session.commit()
    
    except Exception as e:
        flash(f'Erro ao tentar atualizar os preços: {e}', 'alert-danger')
        if session:
            session.rollback()
    
    return redirect(url_for('views.prices'))