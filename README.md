# 🎯 Generador avanzado de códigos QR

Una aplicación desktop profesional para generar y gestionar códigos QR con múltiples funcionalidades avanzadas.

## ✨ Características

### 1. **Generador básico**
- Generar códigos QR desde texto o URLs
- Vista previa en tiempo real
- Validación de URLs automática
- Estadísticas del texto (caracteres, palabras, líneas)
- Múltiples formatos de exportación (PNG, JPG, PDF, BMP, GIF)
- Copiar QR al portapapeles

### 2. **Personalización avanzada**
- Control del nivel de corrección de errores (L, M, Q, H)
- Ajuste de tamaño de caja (1-50)
- Configuración del borde (0-20)
- Versión automática o manual (1-40)
- Selector de colores (primer plano y fondo)
- Agregar logo personalizado al centro del QR

### 3. **Tipos especiales**
- **vCard**: Generar QR con datos de contacto (nombre, teléfono, email, organización, URL)
- **WiFi**: Crear QR para conexión WiFi (SSID, contraseña, seguridad, red oculta)
- **SMS**: Generar QR para enviar mensajes de texto
- **Email**: Crear QR con dirección, asunto y cuerpo del mensaje

### 4. **Códigos de barras**
- Generar códigos de barras tradicionales (CODE128, EAN13)
- Vista previa y guardado

### 5. **Lector de QR**
- Decodificar códigos QR desde archivos de imagen
- Mostrar contenido decodificado

### 6. **Generación por lotes**
- Generar múltiples QR desde archivo CSV
- Procesamiento en lotes con progreso
- Exportación a carpeta personalizada
- Reporte de resultados

### 7. **Historial**
- Mantener historial de últimos 50 QR generados
- Ver detalles de cada generación (timestamp, configuración)
- Limpiar historial completo

### 8. **Gestión de proyectos**
- Guardar proyectos con configuración y historial
- Cargar proyectos guardados
- Eliminar proyectos
- Persistencia en archivos JSON

## 🚀 Instalación

### Requisitos
- Python 3.8+
- pip

### Pasos

1. Clonar o descargar el proyecto
```bash
cd "Generador codigo QR"
```

2. Instalar dependencias
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación
```bash
python Interfaz_Grafica.py
```

## 📦 Dependencias

- **qrcode[pil]**: Generación de códigos QR
- **PyQt6**: Interfaz gráfica
- **Pillow**: Procesamiento de imágenes
- **pyzbar**: Decodificación de QR
- **reportlab**: Exportación a PDF
- **vobject**: Soporte para vCard
- **pyperclip**: Copiar al portapapeles
- **python-barcode**: Generación de códigos de barras

## 📖 Guía de uso

### Pestaña básico
1. Ingrese el texto o URL en el campo de entrada
2. Verifique las estadísticas (caracteres, palabras, líneas)
3. Opcionalmente, active validación de URL para verificar que sea válida
4. Haga clic en "Generar QR"
5. Seleccione el formato y guarde el archivo

### Pestaña personalización
1. Configure los parámetros: nivel de corrección, tamaño, borde, versión
2. Seleccione colores personalizados
3. Opcionalmente, agregue un logo
4. Ingrese el texto en la pestaña Básico
5. Haga clic en "Generar QR personalizado"

### Pestaña especiales
Utilice las diferentes subpestañas para generar:
- **vCard**: Ingrese datos de contacto
- **WiFi**: Ingrese credenciales de red
- **SMS**: Número y mensaje
- **Email**: Dirección, asunto y cuerpo

### Pestaña lector QR
1. Cargue una imagen con código QR
2. El contenido decodificado se mostrará automáticamente

### Pestaña lotes
1. Cargue un archivo CSV (una línea por QR)
2. Seleccione carpeta de salida
3. Haga clic en "Generar lotes"
4. Verifique los resultados en la tabla

### Pestaña proyectos
1. **Guardar**: Guarde la configuración actual como proyecto
2. **Cargar**: Cargue un proyecto guardado
3. **Eliminar**: Borre un proyecto existente

## 🎨 Temas

La aplicación incluye soporte para tema claro y oscuro (configurable en el código).

## 💾 Estructura de archivos

```
Generador codigo QR/
├── Codigo_QR.py              # Lógica principal de generación QR
├── Interfaz_Grafica.py      # Interfaz PyQt6
├── requirements.txt          # Dependencias
├── README.md                 # Este archivo
└── proyectos/               # Carpeta de proyectos guardados
    └── (proyectos.json)
```

## 🔧 Características técnicas

### Generador
- Generación segura de QR con manejo de errores
- Compresión automática de datos
- Soporte para múltiples formatos
- Historial automático de cambios

### Interfaz
- Interfaz modular con pestañas
- Validación de entrada en tiempo real
- Estadísticas en vivo
- Vista previa de resultados

### Storage
- Proyectos guardados en JSON
- Historial persistente en memoria
- Archivos temporales limpios automáticamente

## 📝 Notas importantes

- Los archivos temporales se limpian automáticamente al cerrar la aplicación
- El historial se mantiene en memoria durante la sesión
- Los proyectos se guardan en la carpeta `proyectos/` relativa a la aplicación
- pyzbar requiere librerías del sistema en Linux/Mac

## 🐛 Solución de problemas

**"pyzbar no está instalado"**
- Reinstale pyzbar: `pip install --upgrade pyzbar`
- Windows: Asegúrese de tener Visual C++ Redistributable

**"No se puede cargar imagen"**
- Utilice formatos soportados: PNG, JPG, BMP
- Asegúrese que el QR está visible y bien enfocado

**"Error al generar lotes"**
- Verifique formato CSV (una línea por entrada)
- Compruebe permisos de carpeta de salida

## 📄 Licencia

Proyecto educativo. Libre para usar y modificar.

## 👨‍💻 Autor

Desarrollado con PyQt6 y Python 3

---

**Versión**: 2.0
**Fecha**: Febrero 2026
