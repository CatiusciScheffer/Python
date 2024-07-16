<p> Criar Executável:

<h6>pyinstaller --onefile --noconsole --add-data "templates;templates" --add-data "static;static" app.py

<p> Tornar o app flask em execução em janelas dos sistemas operacionais:

`<h6>`pip install pywebview

<h6> window = webview.create_window('List Book', app) /!* colocar após criar app*/

<h6> webview.start()/!*colocar no init*/
