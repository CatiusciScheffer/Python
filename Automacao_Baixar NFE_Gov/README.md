# Automatização de Download de Notas Fiscais

Este script automatiza o processo de login e download de notas fiscais do site da NFSe. Ele permite que o usuário defina um intervalo de datas para pesquisar as notas, faça o login no site com CNPJ e senha, e faça o download das notas fiscais no formato XML.

## Funcionalidades

* Login automático em um site de emissão de notas fiscais.
* Pesquisa de notas fiscais dentro de um intervalo de datas definido pelo usuário.
* Download automático de notas fiscais e movimentação dos arquivos para uma pasta escolhida.
* Geração de um relatório com o status do download.

## Requisitos

* Python 3.x
* Selenium
* WebDriver Manager
* Pandas
* Tkinter (para a interface gráfica)
* `appdirs` (para gerenciar diretórios de perfil do Chrome)

## Instalação

1. Clone o repositório:
   <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copiar código</button></span></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">git clone https://github.com/CatiusciScheffer/Python/tree/main/Automacao_Baixar%20NFE_Gov
   </code></div></div></pre>
2. Acesse o diretório do projeto:
   <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copiar código</button></span></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">cd automacao-notas-fiscais
   </code></div></div></pre>
3. Instale os pacotes necessários:
   <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copiar código</button></span></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">pip install selenium webdriver-manager pandas appdirs
   </code></div></div></pre>

## Configuração

1. **Perfil do Chrome** : Certifique-se de que o perfil do Chrome usado para login está configurado corretamente. O caminho padrão para o perfil do Chrome é gerado automaticamente, mas você pode ajustar conforme necessário.
2. **Planilha de Notas** : O script faz uso de uma planilha Excel (`AVISO_FGTS.xlsx`) para obter informações sobre os contatos e mensagens.

## Uso

1. Execute o script principal:
   <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copiar código</button></span></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">python script_principal.py
   </code></div></div></pre>
2. Uma interface gráfica será exibida solicitando as seguintes informações:
   * **CNPJ** : O CNPJ usado para login.
   * **SENHA** : A senha de login.
   * **DATA DE INÍCIO (dd/mm/yyyy)** : Data inicial para a pesquisa de notas fiscais.
   * **DATA FIM (dd/mm/yyyy)** : Data final para a pesquisa de notas fiscais.
   * **SALVAR EM** : A pasta onde os arquivos baixados serão salvos.
3. O script abrirá uma janela do navegador, fará login no site, buscará as notas fiscais e fará o download conforme as datas especificadas.

## Funcionalidades do Script

* **Interface Gráfica** : Usando Tkinter, o usuário pode inserir as datas de pesquisa e escolher a pasta de destino.
* **Login Automatizado** : O script faz login no site de notas fiscais usando o CNPJ e senha fornecidos.
* **Pesquisa e Download** : As notas fiscais são pesquisadas dentro do intervalo de datas e baixadas automaticamente.
* **Relatório** : Um arquivo de relatório é gerado para registrar o status do download.
* **Movimentação dos Arquivos** : Os arquivos baixados são movidos para a pasta selecionada pelo usuário.

## Estrutura do Projeto

* `script_principal.py`: Script principal que contém a lógica de automação e interface gráfica.
* `window_parametros.py`: Módulo com a função para obter parâmetros do usuário através da interface gráfica.

## Exemplo de Relatório

O relatório gerado será salvo na pasta de downloads padrão e conterá informações sobre as notas baixadas e o status do processo.

## Contribuições

Contribuições são bem-vindas! Se você tiver sugestões ou encontrar problemas, sinta-se à vontade para abrir uma *issue* ou enviar um  *pull request* .

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE]() para detalhes.
