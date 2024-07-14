from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)






# Modelo para a tabela de livros
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200), nullable=False)
    genero = db.Column(db.String(50))
    ebook = db.Column(db.String(1), default='N')
    fisico = db.Column(db.String(1), default='N')
    inicio = db.Column(db.Date)
    fim = db.Column(db.Date)
    resumo_enredo = db.Column(db.String(3000))
    cenario = db.Column(db.String(300))
    melhor_citacao = db.Column(db.String(300))
    temas_principais = db.Column(db.String(300))
    melhores_personagens = db.Column(db.String(300))
    meu_chips = db.Column(db.String(100))
    analise = db.Column(db.String(3000))
    classificacao = db.Column(db.Integer)

# Rota inicial para exibir a lista de livros
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('book_list.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            titulo = request.form['titulo']
            autor = request.form['autor']
            genero = request.form['genero']
            formato = request.form['formato']
            ebook = 'S' if formato == 'ebook' else 'N'
            fisico = 'S' if formato == 'fisico' else 'N'
            inicio = datetime.strptime(request.form['inicio'], '%Y-%m-%d') if request.form['inicio'] else None
            fim = datetime.strptime(request.form['fim'], '%Y-%m-%d') if request.form['fim'] else None
            resumo_enredo = request.form['resumo_enredo']
            cenario = request.form['cenario']
            melhor_citacao = request.form['melhor_citacao']
            temas_principais = request.form['temas_principais']
            melhores_personagens = request.form['melhores_personagens']
            meu_chips = request.form['meu_chips']
            analise = request.form['analise']
            classificacao = int(request.form['classificacao'])

            new_book = Book(nome=nome, titulo=titulo, autor=autor, genero=genero, ebook=ebook, fisico=fisico,
                            inicio=inicio, fim=fim, resumo_enredo=resumo_enredo, cenario=cenario,
                            melhor_citacao=melhor_citacao, temas_principais=temas_principais,
                            melhores_personagens=melhores_personagens, meu_chips=meu_chips,
                            analise=analise, classificacao=classificacao)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('index'))  # Redireciona para a página inicial após o envio
        except Exception as e:
            print(f"Erro ao adicionar livro: {str(e)}")
            db.session.rollback()  # Desfaz quaisquer mudanças no banco de dados
    
    return render_template('book_form.html')


# Rota para editar um livro específico
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        try:
            book.nome = request.form['nome']
            book.titulo = request.form['titulo']
            book.autor = request.form['autor']
            book.genero = request.form['genero']
            formato = request.form['formato']
            book.ebook = 'S' if formato == 'ebook' else 'N'
            book.fisico = 'S' if formato == 'fisico' else 'N'
            book.inicio = datetime.strptime(request.form['inicio'], '%Y-%m-%d') if request.form['inicio'] else None
            book.fim = datetime.strptime(request.form['fim'], '%Y-%m-%d') if request.form['fim'] else None
            book.resumo_enredo = request.form['resumo_enredo']
            book.cenario = request.form['cenario']
            book.melhor_citacao = request.form['melhor_citacao']
            book.temas_principais = request.form['temas_principais']
            book.melhores_personagens = request.form['melhores_personagens']
            book.meu_chips = request.form['meu_chips']
            book.analise = request.form['analise']
            book.classificacao = int(request.form['classificacao'])

            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Erro ao editar livro: {str(e)}")
            db.session.rollback()

    return render_template('book_form.html', book=book)

# Rota para excluir um livro específico
@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados (só na primeira execução)
    app.run(debug=True)

