from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # debug banco
app.config['SECRET_KEY'] = 'e264a5c0acf609e7f3ac1100562cf084'  # CHAVE SECRETA PARA SEGURANÇA
app.config['COINMARKETCAP_API_KEY'] = '122d6732-65df-475c-8f1d-d7a95ab45bc5'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def create_view():
    with db.engine.connect() as connection:
        connection.execute(text("""
            CREATE VIEW IF NOT EXISTS wallet_summary AS
            SELECT 
                c.name AS cryptocurrency_name,
                wb.balance AS quantity,
                p.price AS price,
                wb.balance * p.price AS total_value
            FROM 
                wallet_balances wb
            JOIN 
                cryptocurrencies c ON wb.cryptocurrency_id = c.id
            JOIN 
                prices p ON wb.cryptocurrency_id = p.cryptocurrency_id
            WHERE 
                wb.wallet_id = :wallet_id;
        """))

def initialize_database():
    with app.app_context():
        db.create_all()  # Cria as tabelas
        create_view()    # Cria a VIEW

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)

from criptoControl import routes

