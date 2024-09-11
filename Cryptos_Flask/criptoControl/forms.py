from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired, Optional, Email, Length, ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
import re


class TransactionsForm(FlaskForm):
    transaction_type = SelectField('Tipo Transação', choices=[('','Selecione o Tipo'), ('Compra','Compra'), ('Venda','Venda'), ('Transferência','Transferência'), ('Saldo','Saldo')], validators=[DataRequired()])
    crypto_payment = SelectField('Moeda', choices=[],validators=[Optional()])
    crypto_payment_price = FloatField('Preço Atual', validators=[Optional()])
    crypto_payment_quantity = FloatField('Quantidade', validators=[Optional()])
    total_paid = FloatField('Total Transação', validators=[Optional()])
    crypto_fee = SelectField('Moeda Taxa', choices=[], validators=[Optional()])
    crypto_fee_price = FloatField('Preço Atual', validators=[Optional()])
    crypto_fee_quantity = FloatField('Quantidade', validators=[Optional()])
    total_fee = FloatField('Total Taxa', validators=[Optional()])
    crypto_receive = SelectField('Moeda Recebida', choices=[],validators=[Optional()])
    crypto_receive_price = FloatField('Preço Atual', validators=[Optional()])
    crypto_receive_quantity = FloatField('Quantidade', validators=[Optional()])
    total_received = FloatField('Total Recebido', validators=[Optional()])
    payment_wallet = SelectField('Carteira Saída', choices=[], validators=[Optional()])
    receiving_wallet = SelectField('Carteira Recebimento', choices=[], validators=[Optional()])
    transaction_date = DateField('Data da Transação', format='%Y-%m-%d', validators=[Optional()])
    btn_add_transactions = SubmitField('Adicionar')


class AddWalletForm(FlaskForm):
    wallet_name = StringField('Nome', validators=[DataRequired()])
    wallet_network = StringField('Rede', validators=[DataRequired()])

class AddCryptoForm(FlaskForm):
    crypto_name = StringField('Nome', validators=[DataRequired()])
    crypto_symbol = StringField('Símbolo', validators=[DataRequired()])

def check_password_complexity(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
    if not re.search(r'[\W_]', password): 
        raise ValidationError('A senha deve conter pelo menos um caractere especial.')

class Users(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Insira um email válido.")])
    password_hash = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=8, message="A senha deve ter pelo menos 8 caracteres."),
        check_password_complexity
    ])
    btn_user_enter = SubmitField('Entrar')