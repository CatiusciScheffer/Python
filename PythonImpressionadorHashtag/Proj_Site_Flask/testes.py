from main import app, database
from models import Usuario, Post


#criar banco de dados
#with app.app_context():
#  database.create_all()

#inserindo informações de usuário no banco de dados
# with app.app_context():
#   usuario = Usuario(username='Catiusci', email='llkpessoal@gmail.com', senha='123456')
#   usuario2 = Usuario(username='Leandro', email='cpcbitencurts@gmail.com', senha='123456')

#   database.session.add(usuario)
#   database.session.add(usuario2)

#   database.session.commit()
  
  
#buscando informações no banco
with app.app_context():
  meus_usuarios = Usuario.query.all()
  meus_primeiro = Usuario.query.first()
  meus_teste = Usuario.query.filter_by(email='llkpessoal@gmail.com').first()
  print(f'{meus_usuarios}: meus_usuarios, {meus_primeiro.username}: primeiro, {meus_teste.email}: filtro')
  
#inserindo informações de post no banco de dados
with app.app_context():
  meu_post = Post(idUser=1)

  database.session.add(usuario)
  database.session.add(usuario2)

  database.session.commit()