from flask import Blueprint, url_for, flash, request, redirect
from criptoControl.models import db, Cryptocurrency, Price
from criptoControl.api import get_crypto_payment_price
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import logging


update_price_bp = Blueprint('update_price', __name__)

logging.basicConfig(level=logging.DEBUG)

def create_session():
    return sessionmaker(bind=db.engine)()


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