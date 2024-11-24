from flask import Blueprint, render_template, send_file
from sqlalchemy import func
from criptoControl.forms import TransactionsForm, AddWalletForm, AddCryptoForm
from criptoControl.models import db, Wallet, Cryptocurrency, WalletBalance, Transaction, Price, User
from flask_login import current_user, login_required
import io
import matplotlib.pyplot as plt


main_bp = Blueprint('main', __name__)


def create_session():
    return sessionmaker(bind=db.engine)()


@main_bp.route('/index')
@login_required  
def index():
    formTransactions = TransactionsForm()
    formAddWallet = AddWalletForm()
    formAddCrypto = AddCryptoForm()
    
    # Inicializa a sessão como None
    session = None
    cons_transactions = []
    cons_wallets = []
    cons_crypto = []

    try:
        session = create_session()
        # Busca as informações no banco
        cons_transactions = session.query(Transaction).all()
        cons_wallets = session.query(Wallet).filter(
            Wallet.wallet_status == 'N',
            Wallet.wallet_user_id == current_user.user_id
        ).all()
        cons_crypto = session.query(Cryptocurrency).filter(Cryptocurrency.crypto_status == 'N').all()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if session:
            session.close()

    return render_template(
        'index.html',
        cons_transactions=cons_transactions,
        cons_wallets=cons_wallets,
        cons_crypto=cons_crypto,
        formTransactions=formTransactions,
        formAddWallet=formAddWallet,
        formAddCrypto=formAddCrypto
    )


@main_bp.route('/grafico')
@login_required
def grafico():
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
        .join(latest_prices_subquery, 
               (Price.price_crypto_id == latest_prices_subquery.c.price_crypto_id) & 
               (Price.price_consult_datetime == latest_prices_subquery.c.latest_timestamp))
        .join(User, User.user_id == Wallet.wallet_user_id)  # Adiciona o join com a tabela User
        .filter(User.user_id == current_user.user_id)       
        .order_by(Wallet.wallet_name, Cryptocurrency.crypto_name)
        .limit(15)
        .all()
    )
    
    # Preparar dados para o gráfico
    data = {}
    for row in query:
        if row.carteira not in data:
            data[row.carteira] = {'x': [], 'y': []}
        # Adiciona os valores corretamente às listas
        data[row.carteira]['x'].append(row.crypto)
        data[row.carteira]['y'].append(row.valor)

    # Gerar o gráfico
    plt.figure(figsize=(10, 6))
    for wallet_name, values in data.items():
        plt.bar(values['x'], values['y'], label=wallet_name)
    
    plt.xlabel('Criptomoeda')
    plt.ylabel('Valor (R$)')
    plt.title('Valor das Criptomoedas por Carteira')
    plt.legend(title='Carteira')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salvar o gráfico em um buffer de memória
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    return send_file(img, mimetype='image/png')
