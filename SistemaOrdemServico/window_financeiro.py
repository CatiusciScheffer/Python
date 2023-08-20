from database import DatabaseManager
import tkinter as tk
from tkinter import Tk, Button, Entry, PhotoImage, Canvas, ttk, messagebox, END, Toplevel

class ManipularWindowFinanceiro():
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def criarTelaFinanceiro(self):
        self.tela_financeiro = Tk()
        self.tela_financeiro.title('Financeiro')
        self.tela_financeiro.geometry("700x400")
        self.tela_financeiro.configure(bg="#204B46")
        
        canvas = Canvas(
            self.tela_financeiro,
            bg="#ffffff",
            height=400,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        
        
        self.tela_financeiro.resizable(False, False)
        self.tela_financeiro.mainloop()