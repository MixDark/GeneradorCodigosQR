# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.0.0] - 2026-02-05

### Agregado
- ✨ Interfaz gráfica completa con PyQt6
- 🎨 Sistema de temas claro/oscuro con botón toggle
- 📱 Generador básico de códigos QR
- 💼 Generador de vCard QR
- 📡 Generador de WiFi QR
- 💬 Generador de SMS QR
- 📧 Generador de Email QR
- 🎨 Personalización avanzada (colores, corrección de errores, tamaño)
- 🖼️ Soporte para agregar logos a los QR
- 📊 Estadísticas en tiempo real (caracteres, palabras, líneas)
- 📋 Historial de últimos 50 QR generados
- 🔍 Lector de códigos QR desde imágenes
- 💾 Descarga de QR en múltiples formatos (PNG, JPG, PDF, BMP, GIF)
- 📋 Copiar QR al portapapeles
- 🌙 Modo oscuro/claro
- 💾 Gestión de proyectos con guardado y carga

### Corregido
- Ajuste de tamaño de previsualizaciones
- Centrado automático de ventana en pantalla
- Escalado proporcional de códigos QR
- Validación de URLs automática

### Tecnología
- Python 3.13+
- PyQt6 6.8.0
- qrcode 8.1+
- python-barcode (opcional)
- pyzbar para lectura de QR
- Pillow para procesamiento de imágenes

## Notas de Desarrollo
- Ventana de 480x770 píxeles, no redimensionable
- Tema oscuro/claro con CSS dinámico
- Sistema de historial con límite de 50 registros
- Generación vCard para crear QR más uniformes

