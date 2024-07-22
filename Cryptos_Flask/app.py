from flask import Flask, render_template, request, redirect, url_for
from models import db, Transacao, Carteira, Cripto, CryptoPrice
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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
        destino = request.form['destino']
        origem = request.form['origem']
        tipo_transacao = request.form['tipo_transacao']

        transacao = Transacao(
            cripto_name=cripto_name,
            quantidade=quantidade,
            preco=preco,
            taxa=taxa,
            date=date,
            destino=destino,
            origem=origem,
            tipo_transacao=tipo_transacao
        )
        db.session.add(transacao)
        db.session.commit()
    except Exception as e:
        # Adicione um tratamento de erro mais sofisticado conforme necessário
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
        print(f"Erro ao adicionar criptomoeda: {e}")
        db.session.rollback()
    return redirect(url_for('moedas'))

if __name__ == '__main__':
    app.run(debug=True)
