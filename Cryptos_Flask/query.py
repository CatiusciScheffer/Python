from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Transacoes(db.Model):
    __tablename__ = 'transacoes'
    id_trans = db.Column(db.Integer, primary_key=True)
    cripto_name = db.Column(db.String(80), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    taxa = db.Column(db.Float, nullable=True)
    date = db.Column(db.Date, nullable=False)
    destino = db.Column(db.String(80), nullable=True)
    origem = db.Column(db.String(80), nullable=False)
    tipo_transacao = db.Column(db.String(80), nullable=False)

@app.route('/test')
def test():
    try:
        transacoes = Transacoes.query.all()
        return f"Transações: {transacoes}"
    except Exception as e:
        return f"Erro ao acessar transações: {e}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
