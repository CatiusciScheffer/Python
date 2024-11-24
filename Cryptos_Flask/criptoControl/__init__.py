from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os


# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)

bootstrap = Bootstrap5(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///crypto_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True 

# Configurar chaves
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma_chave_secreta_padrao')
app.config['COINMARKETCAP_API_KEY'] = os.getenv('COINMARKETCAP_API_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 

@login_manager.user_loader
def load_user(user_id):
    from criptoControl.models import User 
    return User.query.get(int(user_id))

# def initialize_database():
#    with app.app_context():
#        db.create_all()


# Registrar os blueprints
from criptoControl.routes.auth_routes import auth_bp
from criptoControl.routes.transactions_routes import transaction_bp
from criptoControl.routes.main_routes import main_bp
from criptoControl.routes.crud_crypto_wallet import crypto_wallet_bp
from criptoControl.routes.update_price import update_price_bp
from criptoControl.routes.views_databases import views_db_bp

#from criptoControl import routes
app.register_blueprint(auth_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(main_bp)
app.register_blueprint(crypto_wallet_bp)
app.register_blueprint(update_price_bp)
app.register_blueprint(views_db_bp)