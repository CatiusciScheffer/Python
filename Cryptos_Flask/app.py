from flask import Flask, render_template, request, redirect, url_for
from models import db, Transacao, Carteira, Cripto, CryptoPrice, CarteiraSaldo
from datetime import datetime
from flask_migrate import Migrate

migrate = Migrate()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transacoes')
def transacoes():
    transacoes = Transacao.query.all()
    carteiras = Carteira.query.all()
    return render_template('transactions.html', transacoes=transacoes, carteiras=carteiras)

@app.route('/precos')
def precos():
    precos = CryptoPrice.query.all()
    return render_template('prices.html', precos=precos)

@app.route('/carteiras')
def carteiras():
    carteiras = Carteira.query.all()
    return render_template('wallets.html', carteiras=carteiras)

@app.route('/moedas')
def moedas():
    moedas = Cripto.query.all()
    return render_template('cryptos.html', moedas=moedas)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        cripto_name = request.form['cripto_name']
        quantidade = float(request.form['quantidade'])
        preco = float(request.form['preco'])
        taxa = float(request.form.get('taxa', 0))
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        destino_text = request.form['destino_text']
        origem_text = request.form['origem_text']
        tipo_transacao = request.form['tipo_transacao']

        destino_carteira = Carteira.query.filter_by(carteira_nome=destino_text).first()
        origem_carteira = Carteira.query.filter_by(carteira_nome=origem_text).first()
        cripto = Cripto.query.filter_by(cripto_name=cripto_name).first()

        if not destino_carteira or not origem_carteira or not cripto:
            raise Exception("Carteira de origem, destino ou criptomoeda não encontrada")

        origem_saldo = CarteiraSaldo.query.filter_by(carteira_id=origem_carteira.id_carteira, cripto_id=cripto.id_cripto).first()
        destino_saldo = CarteiraSaldo.query.filter_by(carteira_id=destino_carteira.id_carteira, cripto_id=cripto.id_cripto).first()

        if not origem_saldo or not destino_saldo:
            # Cria um novo saldo se não existir
            if not origem_saldo:
                origem_saldo = CarteiraSaldo(carteira_id=origem_carteira.id_carteira, cripto_id=cripto.id_cripto)
                db.session.add(origem_saldo)
            if not destino_saldo:
                destino_saldo = CarteiraSaldo(carteira_id=destino_carteira.id_carteira, cripto_id=cripto.id_cripto)
                db.session.add(destino_saldo)

        if tipo_transacao != 'Venda':
            origem_saldo.saldo -= quantidade
            destino_saldo.saldo += quantidade
        else:
            origem_saldo.saldo += quantidade

        transacao = Transacao(
            cripto_name=cripto_name,
            quantidade=quantidade,
            preco=preco,
            taxa=taxa,
            date=date,
            destino_id=destino_carteira.id_carteira,
            origem_id=origem_carteira.id_carteira,
            tipo_transacao=tipo_transacao
        )

        db.session.add(transacao)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao adicionar transação: {e}")
        db.session.rollback()
    return redirect(url_for('transacoes'))

@app.route('/add_wallet', methods=['POST'])
def add_wallet():
    try:
        carteira_nome = request.form['carteira_nome']
        carteira = Carteira(carteira_nome=carteira_nome)
        db.session.add(carteira)
        db.session.commit()
    except Exception as e:
        # Adicione um tratamento de erro mais sofisticado conforme necessário
        print(f"Erro ao adicionar carteira: {e}")
        db.session.rollback()
    return redirect(url_for('carteiras'))

@app.route('/add_crypto', methods=['POST'])
def add_crypto():
    try:
        cripto_name = request.form['cripto_name']
        cripto_apelido = request.form['cripto_apelido']
        cripto = Cripto(cripto_name=cripto_name, cripto_apelido=cripto_apelido)
        db.session.add(cripto)
        db.session.commit()
    except Exception as e:
        # Adicione um tratamento de erro mais sofisticado conforme necessário
        print(f"Erro ao adicionar cripto: {e}")
        db.session.rollback()
    return redirect(url_for('moedas'))

@app.route('/add_price', methods=['POST'])
def add_price():
    try:
        name = request.form['name']
        price = float(request.form['price'])
        crypto_price = CryptoPrice(name=name, price=price)
        db.session.add(crypto_price)
        db.session.commit()
    except Exception as e:
        # Adicione um tratamento de erro mais sofisticado conforme necessário
        print(f"Erro ao adicionar preço: {e}")
        db.session.rollback()
    return redirect(url_for('precos'))

if __name__ == '__main__':
    app.run(debug=True)