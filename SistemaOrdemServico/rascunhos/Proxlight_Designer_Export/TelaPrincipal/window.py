from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("1000x720")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 720,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    500.0, 360.0,
    image=background_img)
#@@@@@ btn insert
img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 654, y = 187,
    width = 105,
    height = 50)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    120.0, 84.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry0.place(
    x = 69.0, y = 71,
    width = 102.0,
    height = 24)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    168.0, 119.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry1.place(
    x = 115.0, y = 106,
    width = 106.0,
    height = 24)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    151.0, 155.0,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry2.place(
    x = 110.0, y = 142,
    width = 82.0,
    height = 24)

entry3_img = PhotoImage(file = f"img_textBox3.png")
entry3_bg = canvas.create_image(
    348.5, 155.0,
    image = entry3_img)

entry3 = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

entry3.place(
    x = 304.0, y = 142,
    width = 89.0,
    height = 24)

entry4_img = PhotoImage(file = f"img_textBox4.png")
entry4_bg = canvas.create_image(
    534.5, 155.0,
    image = entry4_img)

entry4 = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

entry4.place(
    x = 490.0, y = 142,
    width = 89.0,
    height = 24)

entry5_img = PhotoImage(file = f"img_textBox5.png")
entry5_bg = canvas.create_image(
    711.5, 155.0,
    image = entry5_img)

entry5 = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

entry5.place(
    x = 667.0, y = 142,
    width = 89.0,
    height = 24)

entry6_img = PhotoImage(file = f"img_textBox6.png")
entry6_bg = canvas.create_image(
    550.0, 119.0,
    image = entry6_img)

entry6 = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

entry6.place(
    x = 344.0, y = 106,
    width = 412.0,
    height = 24)

entry7_img = PhotoImage(file = f"img_textBox7.png")
entry7_bg = canvas.create_image(
    319.0, 84.0,
    image = entry7_img)

entry7 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry7.place(
    x = 277.0, y = 71,
    width = 84.0,
    height = 24)

entry8_img = PhotoImage(file = f"img_textBox8.png")
entry8_bg = canvas.create_image(
    595.5, 84.0,
    image = entry8_img)

entry8 = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

entry8.place(
    x = 435.0, y = 71,
    width = 321.0,
    height = 24)

entry9_img = PhotoImage(file = f"img_textBox9.png")
entry9_bg = canvas.create_image(
    327.5, 244.5,
    image = entry9_img)

entry9 = Text(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry9.place(
    x = 30.0, y = 195,
    width = 595.0,
    height = 97)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 654, y = 187,
    width = 105,
    height = 50)
#@@@@@ btn fechamento
img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 654, y = 244,
    width = 105,
    height = 50)
#@@@@@ btn adic cliente
img3 = PhotoImage(file = f"img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 782, y = 71,
    width = 173,
    height = 30)
#@@@@@ btn adic serviço
img4 = PhotoImage(file = f"img4.png")
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b4.place(
    x = 782, y = 109,
    width = 173,
    height = 30)
#@@@@@ btn relatório financeiro
img5 = PhotoImage(file = f"img5.png")
b5 = Button(
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b5.place(
    x = 782, y = 148,
    width = 173,
    height = 30)
#@@@@@ btn modify 
img6 = PhotoImage(file = f"img6.png")
b6 = Button(
    image = img6,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b6.place(
    x = 782, y = 186,
    width = 173,
    height = 30)
#@@@@@ btn delete 
img7 = PhotoImage(file = f"img7.png")
b7 = Button(
    image = img7,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b7.place(
    x = 782, y = 225,
    width = 173,
    height = 30)
#@@@@@ btn imprimir
img8 = PhotoImage(file = f"img8.png")
b8 = Button(
    image = img8,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b8.place(
    x = 782, y = 263,
    width = 173,
    height = 30)

window.resizable(False, False)
window.mainloop()
