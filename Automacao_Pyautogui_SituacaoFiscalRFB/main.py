import tkinter as tk
from tkinter import filedialog
from functions_SituacaoFiscal import LerSituacaoFiscal
import pyautogui

def obter_arquivo_csv():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    file_path = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])

    return file_path

def msgConclusao():
  pyautogui.alert('Tarefa concluída, o computador é seu novamente!')
  
automation = LerSituacaoFiscal()

avisoInicioAutomacao = pyautogui.confirm('Vamos começar a execução do programa, após selecionar a lista de CNPJ não mexa no computador até o programa acabar!')

arquivo_csv = obter_arquivo_csv()
dados = automation.ler_csv(arquivo_csv)

automation.verificarSituacaoFiscalCNPJ(arquivo_csv)

msgConclusao()