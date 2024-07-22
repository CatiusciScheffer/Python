from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import webview

app = Flask(__name__)

window = webview.create_window('List Book', app)  # Converter o app para desktop

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

def create_or_update_book(book, form):
    book.titulo = form['titulo']
    book.autor = form['autor']
    book.genero = form['genero']
    formato = form['formato']
    book.ebook = 'S' if formato == 'ebook' else 'N'
    book.fisico = 'S' if formato == 'fisico' else 'N'
    book.inicio = datetime.strptime(form['inicio'], '%Y-%m-%d') if form['inicio'] else None
    book.fim = datetime.strptime(form['fim'], '%Y-%m-%d') if form['fim'] else None
    book.resumo_enredo = form['resumo_enredo']
    book.cenario = form['cenario']
    book.melhor_citacao = form['melhor_citacao']
    book.temas_principais = form['temas_principais']
    book.melhores_personagens = form['melhores_personagens']
    book.meu_chips = form['meu_chips']
    book.analise = form['analise']
    book.classificacao = int(form['classificacao'])

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('book_list.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        try:
            new_book = Book()
            create_or_update_book(new_book, request.form)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Erro ao adicionar livro: {str(e)}")
            db.session.rollback()
    return render_template('book_form.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        try:
            create_or_update_book(book, request.form)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Erro ao editar livro: {str(e)}")
            db.session.rollback()
    return render_template('book_form.html', book=book)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        webview.start()  # Converter o app para desktop
    app.run(debug=False)
