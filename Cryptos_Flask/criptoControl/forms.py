from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired, Optional, ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class TransacaoForm(FlaskForm):
    tipoTransacao = SelectField('Tipo Transação', choices=[('','Selecione o Tipo'), ('Compra','Compra'), ('Venda','Venda'), ('Transferência','Transferência')], validators=[DataRequired()])
    moedaTransacao = SelectField('Moeda', choices=[],validators=[DataRequired()])
    precoTransacao = FloatField('Preço Atual', validators=[DataRequired()])
    quantidadeTransacao = FloatField('Quantidade', validators=[DataRequired()])
    totalTransacao = FloatField('Total Transacao', validators=[DataRequired()])
    moedaTaxa = SelectField('Moeda Taxa', choices=[], validators=[Optional()])
    precoTaxa = FloatField('Valor Taxa', validators=[Optional()])
    quantidadeTaxa = FloatField('Quantidade', validators=[Optional()])
    totalTaxa = FloatField('Total Taxa', validators=[Optional()])
    carteriaSaidaTransacao = SelectField('Carteira Saída', choices=[], validators=[Optional()])
    carteriaRecebimentoTransacao = SelectField('Carteira Recebimento', choices=[], validators=[Optional()])
    dataTransacao = DateField('Data da Transação', format='%Y-%m-%d', validators=[Optional()])
    adicionarTransacao = SubmitField('Adicionar')

    def validate(self):
        if not super(TransacaoForm, self).validate():
            return False
        
        # Verifica se o tipo de transação é diferente de 'Compra'
        if self.tipoTransacao.data != 'Compra':
            # Valida se os campos de taxa estão preenchidos
            if not self.precoTaxa.data:
                self.precoTaxa.errors.append('Este campo é obrigatório para transações que não sejam do tipo "Compra".')
                return False
            if not self.quantidadeTaxa.data:
                self.quantidadeTaxa.errors.append('Este campo é obrigatório para transações que não sejam do tipo "Compra".')
                return False
            if not self.totalTaxa.data:
                self.totalTaxa.errors.append('Este campo é obrigatório para transações que não sejam do tipo "Compra".')
                return False
        
        return True

class AddWalletForm(FlaskForm):
    nomeCarteira = StringField('Nome', validators=[DataRequired()])
    redeCarteira = StringField('Rede', validators=[DataRequired()])

class AddCryptoForm(FlaskForm):
    nomeMoeda = StringField('Nome', validators=[DataRequired()])
    symbolMoeda = StringField('Símbolo', validators=[DataRequired()])


