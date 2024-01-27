import tkinter as tk
from Codigo_QR import *

class Interfaz(GeneradorCodigoQR):

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Generador codigos QR")
        self.ventana.resizable(0,0)
        self.ancho = 300
        self.alto = 150
        self.ventana_x = ventana.winfo_screenwidth() // 2 - self.ancho // 2
        self.ventana_y = ventana.winfo_screenheight() // 2 - self.alto // 2
        posicion = str(self.ancho) + "x" + str(self.alto) + "+" + str(self.ventana_x) + "+" + str(self.ventana_y)
        self.ventana.geometry(posicion)

        self.mensaje = tk.StringVar()

        self.lbl_texto = tk.Label(ventana, text="Ingrese el texto o la URL",font=("Arial",10,"bold"))
        self.lbl_texto.pack(pady=10)
        self.txt_texto = tk.Entry(ventana, width=50)
        self.txt_texto.pack(padx=10,pady=10)

        self.lbl_mensaje = tk.Label(ventana, textvariable=self.mensaje)
        self.lbl_mensaje.pack(pady=10, side="bottom")

        self.btn_generar = tk.Button(ventana, text="Generar", command=self.generar_qr)
        self.btn_generar.pack(padx=50,side="left")
        self.btn_guardar = tk.Button(ventana, text="Guardar", command=self.guardar_qr, state=tk.DISABLED)
        self.btn_guardar.pack(padx=50,side="right")

ventana = tk.Tk()
aplicacion = Interfaz(ventana)
ventana.mainloop()