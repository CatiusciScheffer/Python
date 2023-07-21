import tkinter as tk
from tkinter import ttk

def set_heading_height(frame, height):
    frame.config(height=height)

root = tk.Tk()

# Crie um frame para o cabeçalho personalizado
header_frame = ttk.Frame(root)
header_frame.pack(fill="x")

treeview = ttk.Treeview(root, columns=("Description", "Value"))
treeview.pack(fill="both", expand=True)

# Adicione as colunas
treeview.heading("#0", text="ID")
treeview.heading("Description", text="Description\n(multiline)", anchor=tk.W)
treeview.heading("Value", text="Value", anchor=tk.W)

# Defina a altura desejada para o cabeçalho personalizado
set_heading_height(header_frame, 60)  # Defina a altura conforme necessário

# Adicione itens de exemplo
treeview.insert("", "end", text="1", values=("First item", "100"))
treeview.insert("", "end", text="2", values=("Second item\n(multiline)", "200"))

root.mainloop()
