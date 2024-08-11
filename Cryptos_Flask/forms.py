from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class TransacaoForm(FlaskForm):
    tipoTransacao = SelectField('Tipo Transação', choices=[('Compra','Compra'), ('Venda','Venda'), ('Transferência','Transferência')], validators=[DataRequired()])
    moedaTransacao = SelectField('Moeda', choices=[],validators=[DataRequired()])
    precoTransacao = FloatField('Preço Atual', validators=[DataRequired()])
    quantidadeTransacao = FloatField('Quantidade', validators=[DataRequired()])
    totalTransacao = FloatField('Total Transacao', validators=[DataRequired()])
    moedaTaxa = SelectField('Moeda Taxa', validators=[DataRequired()])
    precoTaxa = FloatField('Valor Taxa', validators=[DataRequired()])
    quantidadeTaxa = FloatField('Quantidade', validators=[DataRequired()])
    totalTaxa = FloatField('Total Taxa', validators=[DataRequired()])
    carteriaSaidaTransacao = SelectField('Carteira Saída', choices=[], validators=[DataRequired()])
    carteriaRecebimentoTransacao = SelectField('Carteira Recebimento', choices=[],)
    adicionarTransacao = SubmitField('Adicionar')

class AddWalletForm(FlaskForm):
    nomeCarteira = StringField('Nome', validators=[DataRequired()])
    redeCarteira = StringField('Rede', validators=[DataRequired()])

class AddCryptoForm(FlaskForm):
    nomeMoeda = StringField('Nome', validators=[DataRequired()])
    symbolMoeda = StringField('Símbolo', validators=[DataRequired()])


