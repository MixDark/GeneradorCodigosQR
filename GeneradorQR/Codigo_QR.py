import qrcode
import os

class GeneradorCodigoQR:
    def __init__(self):
        self.codigo_qr = None

    def generar_codigo_qr(self, texto):
        if texto:
            try:
                # Configurar y generar el código QR
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(texto)
                qr.make(fit=True)

                # Crear la imagen del código QR
                self.codigo_qr = qr.make_image(fill_color="black", back_color="white")
                
                # Guardar temporalmente la imagen
                temp_path = "temp_qr.png"
                self.codigo_qr.save(temp_path)
                
                return temp_path
            except Exception as e:
                print(f"Error al generar el código QR: {e}")
                return None
        return None

    def guardar_codigo_qr(self, ruta):
        if self.codigo_qr and ruta:
            try:
                self.codigo_qr.save(ruta)
                return True
            except Exception as e:
                print(f"Error al guardar el código QR: {e}")
                return False
        return False

    def __del__(self):
        if os.path.exists("temp_qr.png"):
            try:
                os.remove("temp_qr.png")
            except:
                pass
