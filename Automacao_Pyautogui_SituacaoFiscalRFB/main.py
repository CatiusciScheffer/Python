
import tkinter as tk
from tkinter import filedialog
from functions_SituacaoFiscal_ref import LerSituacaoFiscal
import pyautogui

def obter_arquivo_csv():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    file_path = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])

    return file_path

def msgConclusao():
  pyautogui.alert('AVISO\nTarefa concluída, o computador é seu novamente!')
  pyautogui.hotkey('Ctrl', 'w')
  
automation = LerSituacaoFiscal()

avisoInicioAutomacao = pyautogui.confirm('ATENÇÃO\n''\nSelecione o arquivo(.csv) com a lista de CNPJ\n''\nNÃO MEXA NO COMPUTARDOR ATÉ SER PERMITIDO!')

arquivo_csv = obter_arquivo_csv()
dados = automation.ler_csv(arquivo_csv)

automation.verificarSituacaoFiscalCNPJ(arquivo_csv)

msgConclusao()