import qrcode
import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw
import pyperclip
from urllib.parse import quote

# Manejo de importaciones opcionales
try:
    import barcode
    from barcode.writer import ImageWriter
    BARCODE_AVAILABLE = True
except ImportError:
    BARCODE_AVAILABLE = False

try:
    from pyzbar.pyzbar import decode
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False


class GeneradorCodigoQR:
    def __init__(self):
        self.codigo_qr = None
        self.ultimo_texto = ""
        self.configuracion_actual = {
            'version': None,
            'error_correction': qrcode.constants.ERROR_CORRECT_M,
            'box_size': 10,
            'border': 4,
            'fill_color': 'black',
            'back_color': 'white',
            'con_logo': False,
            'logo_path': None
        }
        self.historial = []
        self.proyectos_guardados = self._cargar_proyectos()
        self.max_historial = 50

    def generar_codigo_qr(self, texto, **kwargs):
        """Genera un código QR con opciones personalizables"""
        if not texto:
            return None

        try:
            # Actualizar configuración
            config = {**self.configuracion_actual}
            config.update(kwargs)
            self.configuracion_actual = config
            self.ultimo_texto = texto

            # Crear QR
            qr = qrcode.QRCode(
                version=config['version'],
                error_correction=config['error_correction'],
                box_size=config['box_size'],
                border=config['border'],
            )
            qr.add_data(texto)
            qr.make(fit=True)

            # Crear imagen
            self.codigo_qr = qr.make_image(
                fill_color=config['fill_color'],
                back_color=config['back_color']
            ).convert('RGB')

            # Agregar logo si se especifica
            if config['con_logo'] and config['logo_path'] and os.path.exists(config['logo_path']):
                self.codigo_qr = self._agregar_logo(self.codigo_qr, config['logo_path'])

            # Guardar temporalmente
            temp_path = "temp_qr.png"
            self.codigo_qr.save(temp_path)

            # Agregar al historial
            self._agregar_al_historial(texto, config)

            return temp_path

        except Exception as e:
            print(f"Error al generar QR: {e}")
            return None

    def _agregar_logo(self, qr_img, logo_path):
        """Agrega un logo al centro del QR"""
        try:
            logo = Image.open(logo_path)
            # Logo ocupa 1/5 del QR
            qr_width, qr_height = qr_img.size
            logo_size = min(qr_width, qr_height) // 5
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Crear fondo blanco para el logo
            logo_bg = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
            logo_bg.paste(logo, (10, 10))

            # Pegar logo en el centro
            logo_pos = ((qr_width - logo_size - 20) // 2, (qr_height - logo_size - 20) // 2)
            qr_img.paste(logo_bg, logo_pos)

            return qr_img
        except Exception as e:
            print(f"Error al agregar logo: {e}")
            return qr_img

    def guardar_codigo_qr(self, ruta, formato='PNG'):
        """Guarda el QR en diferentes formatos"""
        if not self.codigo_qr or not ruta:
            return False

        try:
            formato = formato.upper()

            if formato == 'PNG':
                self.codigo_qr.save(ruta, 'PNG')
            elif formato == 'JPG' or formato == 'JPEG':
                self.codigo_qr.save(ruta, 'JPEG', quality=95)
            elif formato == 'PDF':
                self.codigo_qr.save(ruta, 'PDF')
            elif formato == 'BMP':
                self.codigo_qr.save(ruta, 'BMP')
            elif formato == 'GIF':
                self.codigo_qr.save(ruta, 'GIF')
            else:
                self.codigo_qr.save(ruta)

            return True
        except Exception as e:
            print(f"Error al guardar QR: {e}")
            return False

    def generar_vcard(self, nombre, telefono='', email='', organizacion='', url=''):
        """Genera un código QR con datos de contacto vCard"""
        try:
            vcard_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{nombre}\n"
            if telefono:
                vcard_data += f"TEL:{telefono}\n"
            if email:
                vcard_data += f"EMAIL:{email}\n"
            if organizacion:
                vcard_data += f"ORG:{organizacion}\n"
            if url:
                vcard_data += f"URL:{url}\n"
            vcard_data += "END:VCARD"

            return self.generar_codigo_qr(vcard_data)
        except Exception as e:
            print(f"Error al generar vCard: {e}")
            return None

    def generar_wifi(self, ssid, password, security='WPA', hidden=False):
        """Genera un código QR para conexión WiFi"""
        try:
            wifi_data = f"WIFI:T:{security};S:{ssid};P:{password};H:{'true' if hidden else 'false'};;"
            return self.generar_codigo_qr(wifi_data)
        except Exception as e:
            print(f"Error al generar WiFi QR: {e}")
            return None

    def generar_sms(self, numero, mensaje=''):
        """Genera un código QR para enviar SMS"""
        try:
            sms_data = f"smsto:{numero}"
            if mensaje:
                sms_data += f":{quote(mensaje)}"
            return self.generar_codigo_qr(sms_data)
        except Exception as e:
            print(f"Error al generar SMS QR: {e}")
            return None

    def generar_email(self, email, asunto='', cuerpo=''):
        """Genera un código QR para enviar correo"""
        try:
            mailto = f"mailto:{email}"
            params = []
            if asunto:
                params.append(f"subject={quote(asunto)}")
            if cuerpo:
                params.append(f"body={quote(cuerpo)}")
            if params:
                mailto += "?" + "&".join(params)
            return self.generar_codigo_qr(mailto)
        except Exception as e:
            print(f"Error al generar Email QR: {e}")
            return None

    def generar_codigo_barras(self, numero, tipo='code128'):
        """Genera un código de barras tradicional"""
        if not BARCODE_AVAILABLE:
            print("Error: python-barcode no está instalado")
            return None
        
        try:
            if tipo.lower() == 'code128':
                barcode_class = barcode.get_barcode_class('code128')
            elif tipo.lower() == 'ean13':
                barcode_class = barcode.get_barcode_class('ean13')
            else:
                barcode_class = barcode.get_barcode_class('code128')

            bar = barcode_class(numero, writer=ImageWriter())
            temp_path = 'temp_barcode'
            bar.save(temp_path)
            return f'{temp_path}.png'
        except Exception as e:
            print(f"Error al generar código de barras: {e}")
            return None

    def decodificar_qr(self, ruta_imagen):
        """Decodifica un código QR desde una imagen"""
        if not PYZBAR_AVAILABLE:
            return None, "pyzbar no está instalado"

        try:
            imagen = Image.open(ruta_imagen)
            resultados = decode(imagen)

            if resultados:
                textos = [resultado.data.decode('utf-8') for resultado in resultados]
                return textos, "OK"
            else:
                return None, "No se encontró código QR en la imagen"

        except Exception as e:
            return None, f"Error al decodificar: {e}"

    def generar_lote_desde_csv(self, ruta_csv, carpeta_salida, config=None):
        """Genera múltiples QR desde un archivo CSV"""
        try:
            if not os.path.exists(carpeta_salida):
                os.makedirs(carpeta_salida)

            resultados = []
            with open(ruta_csv, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    if linea:
                        nombre_archivo = f"{linea[:30].replace(' ', '_')}.png"
                        ruta_salida = os.path.join(carpeta_salida, nombre_archivo)

                        if self.generar_codigo_qr(linea):
                            if self.guardar_codigo_qr(ruta_salida):
                                resultados.append((linea, True, ruta_salida))
                            else:
                                resultados.append((linea, False, "Error al guardar"))
                        else:
                            resultados.append((linea, False, "Error al generar"))

            return resultados
        except Exception as e:
            print(f"Error en lote: {e}")
            return []

    def copiar_al_portapapeles(self):
        """Copia el QR actual al portapapeles"""
        try:
            if self.codigo_qr:
                temp_path = "temp_clipboard.png"
                self.codigo_qr.save(temp_path)
                # Nota: pyperclip no maneja imágenes bien en Windows, se devuelve la ruta
                pyperclip.copy(temp_path)
                return True
        except Exception as e:
            print(f"Error al copiar: {e}")
            return False

    def _agregar_al_historial(self, texto, config):
        """Agrega un QR al historial"""
        entrada = {
            'timestamp': datetime.now().isoformat(),
            'texto': texto,
            'config': config,
            'tipo': 'QR'
        }
        self.historial.insert(0, entrada)
        if len(self.historial) > self.max_historial:
            self.historial = self.historial[:self.max_historial]

    def obtener_historial(self):
        """Retorna el historial"""
        return self.historial

    def limpiar_historial(self):
        """Limpia el historial"""
        self.historial = []

    def guardar_proyecto(self, nombre_proyecto):
        """Guarda el proyecto actual"""
        try:
            proyecto = {
                'nombre': nombre_proyecto,
                'timestamp': datetime.now().isoformat(),
                'texto_actual': self.ultimo_texto,
                'configuracion': self.configuracion_actual,
                'historial': self.historial
            }

            carpeta_proyectos = Path('proyectos')
            carpeta_proyectos.mkdir(exist_ok=True)

            ruta_proyecto = carpeta_proyectos / f"{nombre_proyecto}.json"
            with open(ruta_proyecto, 'w', encoding='utf-8') as f:
                json.dump(proyecto, f, indent=2, ensure_ascii=False)

            self.proyectos_guardados[nombre_proyecto] = {
                'ruta': str(ruta_proyecto),
                'timestamp': proyecto['timestamp']
            }
            return True
        except Exception as e:
            print(f"Error al guardar proyecto: {e}")
            return False

    def cargar_proyecto(self, nombre_proyecto):
        """Carga un proyecto guardado"""
        try:
            if nombre_proyecto not in self.proyectos_guardados:
                return False

            ruta_proyecto = self.proyectos_guardados[nombre_proyecto]['ruta']
            with open(ruta_proyecto, 'r', encoding='utf-8') as f:
                proyecto = json.load(f)

            self.ultimo_texto = proyecto['texto_actual']
            self.configuracion_actual = proyecto['configuracion']
            self.historial = proyecto['historial']
            return True
        except Exception as e:
            print(f"Error al cargar proyecto: {e}")
            return False

    def obtener_proyectos(self):
        """Retorna lista de proyectos guardados"""
        return list(self.proyectos_guardados.keys())

    def eliminar_proyecto(self, nombre_proyecto):
        """Elimina un proyecto guardado"""
        try:
            if nombre_proyecto in self.proyectos_guardados:
                ruta_proyecto = self.proyectos_guardados[nombre_proyecto]['ruta']
                if os.path.exists(ruta_proyecto):
                    os.remove(ruta_proyecto)
                del self.proyectos_guardados[nombre_proyecto]
                self._guardar_index_proyectos()
                return True
        except Exception as e:
            print(f"Error al eliminar proyecto: {e}")
            return False

    def _cargar_proyectos(self):
        """Carga el índice de proyectos guardados"""
        try:
            carpeta_proyectos = Path('proyectos')
            proyectos = {}

            if carpeta_proyectos.exists():
                for archivo_json in carpeta_proyectos.glob('*.json'):
                    nombre = archivo_json.stem
                    proyectos[nombre] = {
                        'ruta': str(archivo_json),
                        'timestamp': archivo_json.stat().st_mtime
                    }

            return proyectos
        except:
            return {}

    def _guardar_index_proyectos(self):
        """Actualiza el índice de proyectos"""
        self.proyectos_guardados = self._cargar_proyectos()

    def obtener_estadisticas(self, texto):
        """Retorna estadísticas del texto"""
        return {
            'caracteres': len(texto),
            'caracteres_sin_espacios': len(texto.replace(' ', '')),
            'palabras': len(texto.split()),
            'lineas': len(texto.split('\n'))
        }

    def validar_url(self, url):
        """Valida si una URL es válida"""
        try:
            from urllib.parse import urlparse
            resultado = urlparse(url)
            return all([resultado.scheme, resultado.netloc])
        except:
            return False

    def __del__(self):
        """Limpia archivos temporales"""
        archivos_temp = ['temp_qr.png', 'temp_clipboard.png', 'temp_barcode.png']
        for archivo in archivos_temp:
            if os.path.exists(archivo):
                try:
                    os.remove(archivo)
                except:
                    pass
