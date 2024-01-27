import qrcode
import tkinter as tk
from tkinter import filedialog

class GeneradorCodigoQR:
    
    def generar_qr(self):
        dato = self.txt_texto.get()
        if dato:
            self.codigo_qr = qrcode.make(dato)
            self.btn_guardar.config(state=tk.NORMAL)
            self.mensaje.set("Código QR generado correctamente")
        else:
            self.codigo_qr  = None
            self.btn_guardar.config(state=tk.DISABLED)

    def guardar_qr(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".png")
        if ruta:
            self.codigo_qr.save(ruta)