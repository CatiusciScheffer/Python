from typing import Optional, Tuple, Union
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import openpyxl, xlrd
import pathlib
from openpyxl import Workbook

# Mudando a aparência do sistema
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class App(ctk.CTk):
  def __init__(self):
    super().__init__() # classe principal do sistema
    self.layout_config()
    self.appearence()
    self.todo_sistema()
  
  
  def layout_config(self):
    self.title('Sistema de Cadastro de Clientes')
    self.geometry('700x500')
    
  def appearence(self):
    self.lbamp = ctk.CTkLabel(self,text='Tema', bg_color='transparent', text_color=['#000', '#fff']).place(x=50, y=430)
    self.opt_apm= ctk.CTkOptionMenu(self, values=['Light', 'Dark', 'System'], command=self.change_apm).place(x=50, y=460)

    
  
  
  def todo_sistema(self):
    frame = ctk.CTkFrame(self, width = 700, height = 50, corner_radius = 0, bg_color = 'DeepSkyBlue2', fg_color = 'DeepSkyBlue2')
    frame.place(x = 0, y=0)
    title = ctk.CTkLabel(frame, text='Cadastro de Clientes', font=('Century Gothic bold', 24), text_color='#fff').place(relx=0.5, rely=0.5, anchor='center')
    
    span = title = ctk.CTkLabel(self, text='*Preencha todos os campos do formulário!', font=('Century Gothic bold', 12), text_color=['#000', '#fff']).place(relx=0.5, y=70, anchor='center')
  
  
  
  def change_apm(self, nova_aparencia):
    ctk.set_appearance_mode(nova_aparencia)
  
  
  
  
    
if __name__=='__main__':
  app = App()
  app.mainloop()