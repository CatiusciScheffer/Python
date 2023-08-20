from tkinter import *
import xmltodict
import json
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog

def selecionar_pasta_input():
    pasta_input = filedialog.askdirectory()
    input_dir_var.set(pasta_input)

def selecionar_pasta_output():
    pasta_output = filedialog.askdirectory()
    output_dir_var.set(pasta_output)

def processar_xml():
    try:
        pasta_input = input_dir_var.get()
        pasta_output = output_dir_var.get()

        dataframes = []

        for nome_arquivo in os.listdir(pasta_input):
            caminho_arquivo = os.path.join(pasta_input, nome_arquivo)

            if nome_arquivo.endswith('.xml'):
                with open(caminho_arquivo, 'rb') as arquivo:
                    documento = xmltodict.parse(arquivo)
                    documento_json = json.dumps(documento, indent=2, ensure_ascii=False)
                    data = json.loads(documento_json)
                    df = pd.json_normalize(data)
                    dataframes.append(df)

        df_final = pd.concat(dataframes, ignore_index=True)
        output_filename = os.path.join(pasta_output, 'saida.xlsx')
        df_final.to_excel(output_filename, index=False)
        status_label.config(text=f'Dados exportados para {output_filename}')
    except Exception as e:
        return status_label.config(text=f'Não existe arquivo XML nesta pasta.')

window = Tk()

window.geometry("496x315")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 315,
    width = 496,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

input_dir_var = tk.StringVar()
output_dir_var = tk.StringVar()

background_img = PhotoImage(file = f"./img/background.png")
background = canvas.create_image(
    248.0, 157.5,
    image=background_img)

img0 = PhotoImage(file = f"./img/btn_selecionar.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = selecionar_pasta_input,
    relief = "flat")

b0.place(
    x = 299, y = 68,
    width = 116,
    height = 30)

img1 = PhotoImage(file = f"./img/btn_salvar.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = selecionar_pasta_output,
    relief = "flat")

b1.place(
    x = 299, y = 143,
    width = 116,
    height = 30)

img2 = PhotoImage(file = f"./img/btn_executar.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = processar_xml,
    relief = "flat")

b2.place(
    x = 183, y = 207,
    width = 116,
    height = 46)

status_label = tk.Label(window, text="", bg= '#202020', fg='white')
status_label.place(
    x = 34, y = 280,
    width = 434,
    height = 25
)

window.resizable(False, False)
window.mainloop()
