 
from criptoControl import app
import webview
from threading import Thread

def run_flask():
    app.run(debug=True, use_reloader=False)  # use_reloader=False evita que Flask seja iniciado duas vezes

if __name__ == '__main__':
    # Inicia o servidor Flask em uma thread separada
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True  # Thread daemons são encerradas automaticamente quando o programa principal encerra
    flask_thread.start()

    # Abre a janela do navegador embutido usando pywebview
    webview.create_window('Crypto_Control', 'http://127.0.0.1:5000')  # URL do servidor Flask
    webview.start()
