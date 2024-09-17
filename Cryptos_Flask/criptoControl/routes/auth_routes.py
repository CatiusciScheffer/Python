from flask import Blueprint, render_template, flash, redirect, url_for
from criptoControl.forms import Users
from criptoControl.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user
from criptoControl import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    formLogin = Users()  # Formulário de login

    if formLogin.validate_on_submit():
        # Verifica se o email existe no banco de dados
        user = User.query.filter_by(email=formLogin.email.data).first()
        if user and check_password_hash(user.password_hash, formLogin.password_hash.data):
            # Se o email e a senha são válidos, faz o login do usuário
            login_user(user)
            flash('Login bem-sucedido!', 'alert-success')
            return redirect(url_for('main.index'))  # Redireciona para a rota index após o login
        else:
            flash('Credenciais inválidas. Verifique seu email e senha.', 'alert-danger')

    return render_template('auth/login.html', formLogin=formLogin)