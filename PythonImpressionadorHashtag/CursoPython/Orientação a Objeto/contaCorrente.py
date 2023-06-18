from datetime import datetime
import pytz


class ContaCorrente:
  
  @staticmethod
  def _data_hora():
    fuso_BR = pytz.timezone('Brazil/East')
    horario_BR = datetime.now(fuso_BR)
    return horario_BR.strftime(' %d/%m/%Y     %H:%M:%S')
  
  def __init__(self, nome, cpf, agencia, num_conta):
    self._nome = nome
    self._cpf = cpf
    self._saldo = 0
    self._limite = 0
    self._agencia = agencia
    self._num_conta = num_conta
    self._transacoes = []
    self._cartoes = []
    
  def consultar_saldo(self):
    print('\n','-' * 19, ' Extrato Consolidado ', '_' * 19, '\n')
    print(f'Saldo da Conta     R$ {self._saldo:,.2f}\nLimite Disponível  R$ {((self._limite_conta() - self._saldo) * -1):,.2f}')
    
  def depositar(self, valor):
    self._saldo += valor
    print(f'Depósito       R$ +{valor:,.2f}')
    self._transacoes.append((f'{ContaCorrente._data_hora()}     +{valor:,.2f}     {self._saldo:,.2f}'))
  
  def _limite_conta(self):
    self._limite = -1000
    return self._limite
    
  def sacar(self, valor):
    if self._saldo - valor < self._limite_conta():
      print(f'Saldo insuficiente, valor disponível para saque é R$ {(self._saldo - self._limite_conta()):,.2f}')
    else:
      self._saldo -= valor
      print(f'Saque          R$ -{valor:,.2f}')
      self._transacoes.append((f'{ContaCorrente._data_hora()}     -{valor:,.2f}      {self._saldo:,.2f}'))
  
  def consultar_limite_chequeespecial(self):
    print(f'Seu limite no cheque especial é de R$ {self._limite_conta():,.2f}')
    
  def consultar_historico_transacoes(self):
    print('_' * 18,' Histórico de Transações ', '_' * 18, '\n')
    print('|    DATA    |    HORA    |   VALOR   |   SALDO   |')
    transacao = [print(f'{transacao}') for transacao in self._transacoes]
    return transacao
  
  def transferir(self, valor,conta_destino):
    self.saldo -= valor
    self._transacoes.append((-valor, self._saldo, ContaCorrente._data_hora()))
    conta_destino._saldo += valor
    conta_destino._transacoes.append((valor, conta_destino._saldo, ContaCorrente._data_hora()))
    
class CartaoCredito:
  
  def __init__(self, titular, conta_corrente):
    self.numeroCCredito = 146
    self.titularCCredito = titular
    self.validadeCCredito = None
    self.codSegCCredito = None
    self.limiteCCredito = None
    self.numCtaCorrente = conta_corrente
    conta_corrente._cartoes.append(self)
    
    
conta_Catiusci = ContaCorrente('Catiusci P.C.Scheffer', '001.162.860-08', 291, 1359658)

cartao_Catiusci = CartaoCredito('Catiusci', conta_Catiusci)

print(cartao_Catiusci.numCtaCorrente._num_conta)

print(conta_Catiusci._cartoes) #printa o objeto

print(conta_Catiusci._cartoes[0]) #remove os []

print(conta_Catiusci._cartoes[0].numeroCCredito) #agora printa o atributo da classe CartãoCredito


