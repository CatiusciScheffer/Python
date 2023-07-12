from main import database
from datetime import datetime

"""quero criar uma relação de 1 usuário para * posts, uma relação 1/*:
  crio a relação com relationchip dentro da tabela de 1,neste caso da tabela usuário
  e na tabela de * no caso Post crio a chave estrangeira
"""
class Usuario(database.Model):
  idUser = database.Column(database.Integer, primary_key=True)
  username = database.Column(database.String, nullable=False)
  email = database.Column(database.String, nullable=False, unique=True)
  senha = database.Column(database.String, nullable=False)
  foto_perfil = database.Column(database.String, default='default.jpg')
  cusros = database.Column(database.String, nullable=False,default='Não Informado')
  posts = database.relationship('Post', backref='autor', lazy=True)
  # criando a relação,no parênteses vai a tabela, backref = o que eu quero pegar nas consultas posteriores, lazy utilizo para fazer a consulta direta posteriormente
  
class Post(database.Model):
  idPost = database.Column(database.Integer, primary_key=True)
  titulo = database.Column(database.String, nullable=False)
  corpo = database.Column(database.Text, nullable=False)
  data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
  idUser = database.Column(database.Integer, database.ForeignKey('usuario.idUser'), nullable=False)
  #criando a chave estrangeira,entre parênteses coloco a (classe em letra minúscula.coluna da tabela)
  