from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

class TransacaoForm(FlaskForm):
    tipoTransacao = SelectField('Tipo Transacao', choices=[('Compra','Compra'), ('Venda','Venda'), ('Transferência','Transferência')], validators=[DataRequired()])
    moedaTransacao = SelectField('Moeda', validators=[DataRequired()])
    precoTransacao = FloatField('Preço na Transação', validators=[DataRequired()])
    quantidadeTransacao = FloatField('Quantidade', validators=[DataRequired()])
    moedaTaxa = SelectField('Moeda para pagar Taxa', validators=[DataRequired()])
    valorTaxa = FloatField('Valor Taxa', validators=[DataRequired()])
    carteriaOrigemTransacao = SelectField('Carteira Origem', validators=[DataRequired()])
    carteriaRecebimentoTransacao = SelectField('Carteira Recebimento')
    adicionarTransacao = SubmitField('Adicionar')