from flask import Blueprint, render_template, url_for, flash, request, redirect
from sqlalchemy import or_
from criptoControl.forms import AddWalletForm, AddCryptoForm
from criptoControl.models import db, Wallet, Cryptocurrency, Transaction
from flask_login import current_user, login_required
import logging

crypto_wallet_bp = Blueprint('crypto_wallet', __name__)

logging.basicConfig(level=logging.DEBUG)

# Adicionar Carteira
@crypto_wallet_bp.route('/add_wallet', methods=['GET', 'POST'])
@login_required
def add_wallet():
    formAddWallet = AddWalletForm()  # Criação do formulário
    if formAddWallet.validate_on_submit():
        wallet_name = formAddWallet.wallet_name.data.strip().upper()
        wallet_network = formAddWallet.wallet_network.data.strip().upper()
        try:
            wallet = Wallet(wallet_user_id=current_user.user_id, wallet_name=wallet_name, wallet_network=wallet_network)
            db.session.add(wallet)
            db.session.commit()
            flash(f'A Carteira {wallet_name} foi adicionada com sucesso', 'alert-success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao tentar adicionar a carteira: {e}', 'alert-danger')
        return redirect(url_for('views.wallets'))

    return render_template('operacoes/add_wallet.html', formAddWallet=formAddWallet)


# Remover Carteira
@crypto_wallet_bp.route('/delete_wallet', methods=['POST'])
@login_required
def delete_wallet():
    wallet_id = request.form.get('wallet_id')
    if wallet_id:
        try:
            wallet = Wallet.query.filter_by(wallet_id=wallet_id, wallet_user_id=current_user.user_id).first()
            if not wallet:
                flash('Carteira não encontrada.', 'alert-danger')
                return redirect(url_for('views.wallets'))

            wallet_in_transactions = Transaction.query.filter(
                or_(
                    Transaction.payment_wallet_id == wallet_id,
                    Transaction.receiving_wallet_id == wallet_id
                )
            ).first()

            if not wallet_in_transactions:
                db.session.delete(wallet)
                db.session.commit()
                flash('Carteira deletada com sucesso.', 'alert-success')
            else:
                wallet.wallet_status = 'S'
                db.session.commit()
                flash('Carteira desativada pois já tiveram transações com ela.', 'alert-success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao tentar desativar a carteira: {e}', 'alert-danger')
    else:
        flash("ID da carteira não fornecido", 'alert-danger')
    
    return redirect(url_for('views.wallets'))

# Adicionar Moeda
@crypto_wallet_bp.route('/add_crypto', methods=['GET', 'POST'])
@login_required
def add_crypto():
    formAddCrypto = AddCryptoForm()
    if formAddCrypto.validate_on_submit():
        crypto_name = formAddCrypto.crypto_name.data.strip().upper()
        crypto_symbol = formAddCrypto.crypto_symbol.data.strip().upper()
        try:
            crypto = Cryptocurrency(crypto_name=crypto_name, crypto_symbol=crypto_symbol)
            db.session.add(crypto)
            db.session.commit()
            flash(f'A Criptomoeda {crypto_name} foi adicionada com sucesso', 'alert-success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao tentar adicionar a criptomoeda: {e}', 'alert-danger')
        return redirect(url_for('views.cryptos'))

    return render_template('operacoes/add_crypto.html', formAddCrypto=formAddCrypto)

# Remover Moeda
@crypto_wallet_bp.route('/delete_crypto', methods=['POST'])
@login_required
def delete_crypto():
    crypto_id = request.form.get('crypto_id')
    if crypto_id:
        try:
            crypto = Cryptocurrency.query.filter_by(crypto_id=crypto_id).first()
            if not crypto:
                flash('Criptomoeda não encontrada.', 'alert-danger')
                return redirect(url_for('views.cryptos'))

            crypto_in_transaction = Transaction.query.filter(
                or_(
                    Transaction.crypto_payment_id == crypto.crypto_id,
                    Transaction.crypto_receive_id == crypto.crypto_id,
                    Transaction.crypto_fee_id == crypto.crypto_id
                )
            ).first()

            if not crypto_in_transaction:
                db.session.delete(crypto)
                db.session.commit()
                flash('Criptomoeda deletada com sucesso.', 'alert-success')
            else:
                crypto.crypto_status = 'S'
                db.session.commit()
                flash('Criptomoeda apenas desativada, pois teve transações com ela.', 'alert-success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao tentar desativar a criptomoeda: {e}', 'alert-danger')
    else:
        flash("ID da criptomoeda não fornecido", 'alert-danger')
    
    return redirect(url_for('views.cryptos'))

