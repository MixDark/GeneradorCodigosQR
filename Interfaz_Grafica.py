import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QFileDialog, QTabWidget,
                            QSpinBox, QComboBox, QCheckBox, QColorDialog, QListWidget,
                            QListWidgetItem, QInputDialog, QMessageBox, QScrollArea,
                            QGridLayout, QTextEdit, QTableWidget, QTableWidgetItem,
                            QProgressBar, QDialog, QDialogButtonBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QColor
from Codigo_QR import GeneradorCodigoQR, BARCODE_AVAILABLE
from estilos import ESTILO_OSCURO, ESTILO_CLARO
import qrcode


class DialogoGuardarProyecto(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guardar proyecto")
        self.setGeometry(100, 100, 300, 150)
        
        layout = QVBoxLayout()
        
        label = QLabel("Nombre del proyecto:")
        self.nombre_input = QLineEdit()
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Guardar")
        cancel_button = QPushButton("Cancelar")
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        layout.addWidget(label)
        layout.addWidget(self.nombre_input)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)


class InterfazQR(QMainWindow):
    def __init__(self):
        super().__init__()
        self.generador = GeneradorCodigoQR()
        self.tema_oscuro = False
        self.initUI()
        self.aplicar_estilo()
        
    def initUI(self):
        self.setWindowTitle('Generador códigos QR')
        
        # Centrar la ventana
        screen = QApplication.primaryScreen().geometry()
        width, height = 480, 770
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        
        self.setGeometry(x, y, width, height)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.setWindowIcon(QIcon('icono.png'))
        
        # Widget central con tabs y botón de modo oscuro
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tabs = QTabWidget()
        
        # Crear tabs
        self.tab_basico = self.crear_tab_basico()
        self.tab_personalizacion = self.crear_tab_personalizacion()
        self.tab_especiales = self.crear_tab_especiales()
        self.tab_lector = self.crear_tab_lector()
        self.tab_historial = self.crear_tab_historial()
        
        self.tabs.addTab(self.tab_basico, "Básico")
        self.tabs.addTab(self.tab_personalizacion, "Personalización")
        self.tabs.addTab(self.tab_especiales, "Especiales")
        self.tabs.addTab(self.tab_lector, "Lector QR")
        self.tabs.addTab(self.tab_historial, "Historial")
        
        main_layout.addWidget(self.tabs)
        
        # Botón de modo oscuro en la esquina inferior derecha
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.boton_tema = QPushButton("🌙")
        self.boton_tema.setMaximumWidth(45)
        self.boton_tema.setMaximumHeight(35)
        self.boton_tema.setToolTip("Modo oscuro/claro")
        self.boton_tema.clicked.connect(self.cambiar_tema)
        button_layout.addWidget(self.boton_tema)
        button_layout.setContentsMargins(8, 5, 8, 5)
        main_layout.addLayout(button_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def crear_tab_basico(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Entrada de texto
        label = QLabel("Ingrese el texto o la URL:")
        self.text_input = QLineEdit()
        self.text_input.setMinimumHeight(36)
        self.text_input.setMaximumHeight(40)
        self.text_input.textChanged.connect(self.actualizar_estadisticas)
        
        # Estadísticas
        self.stats_label = QLabel("Caracteres: 0 | Palabras: 0 | Líneas: 1")
        self.stats_label.setStyleSheet("color: #666666; font-size: 10px;")
        
        # Validador y Formato en una fila
        validar_formato_layout = QHBoxLayout()
        validar_formato_layout.setSpacing(4)
        validar_formato_layout.setContentsMargins(0, 0, 0, 0)
        self.validar_url_check = QCheckBox("Validar URL")
        self.url_status_label = QLabel("")
        validar_formato_layout.addWidget(self.validar_url_check)
        validar_formato_layout.addWidget(self.url_status_label)
        
        validar_formato_layout.addSpacing(10)
        validar_formato_layout.addWidget(QLabel("Formato:"))
        self.formato_combo = QComboBox()
        self.formato_combo.setMaximumWidth(100)
        self.formato_combo.addItems(['PNG', 'JPG', 'PDF', 'BMP', 'GIF'])
        validar_formato_layout.addWidget(self.formato_combo)
        validar_formato_layout.addStretch()
        
        # Mostrar QR
        self.qr_preview = QLabel()
        self.qr_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_preview.setMinimumSize(280, 280)
        self.qr_preview.setMaximumSize(350, 350)
        self.qr_preview.setStyleSheet("border: 1px solid #cccccc;")
        
        # Botones debajo del preview
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.setContentsMargins(0, 0, 0, 0)
        generar_button = QPushButton("Generar QR")
        copiar_button = QPushButton("Copiar al portapapeles")
        guardar_button = QPushButton("Guardar")
        
        generar_button.setMaximumWidth(140)
        copiar_button.setMaximumWidth(160)
        guardar_button.setMaximumWidth(110)
        
        generar_button.setMinimumHeight(36)
        copiar_button.setMinimumHeight(36)
        guardar_button.setMinimumHeight(36)
        
        generar_button.clicked.connect(self.generar_qr_basico)
        copiar_button.clicked.connect(self.copiar_qr)
        guardar_button.clicked.connect(self.guardar_qr)
        
        button_layout.addWidget(generar_button)
        button_layout.addWidget(copiar_button)
        button_layout.addWidget(guardar_button)
        
        # Estado
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Armar el layout
        layout.setSpacing(0)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Layout para juntar label y input sin espaciado
        input_layout = QVBoxLayout()
        input_layout.setSpacing(0)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.addWidget(label)
        input_layout.addWidget(self.text_input)
        layout.addLayout(input_layout)
        
        layout.addWidget(self.stats_label)
        layout.addWidget(QLabel(""))  # Espacio mínimo
        layout.addLayout(validar_formato_layout)
        layout.addSpacing(20)
        layout.addWidget(self.qr_preview, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(12)
        layout.addLayout(button_layout)
        layout.addSpacing(12)
        layout.addWidget(self.status_label)
        
        widget.setLayout(layout)
        return widget

    def crear_tab_personalizacion(self):
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        # ScrollArea para contenido largo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumWidth(440)
        scroll_widget = QWidget()
        scroll_widget.setMinimumWidth(430)
        layout = QVBoxLayout()
        layout.setSpacing(22)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # FILA 1: Nivel de corrección, Tamaño de caja, Borde
        row1 = QHBoxLayout()
        row1.setSpacing(50)
        row1.setContentsMargins(0, 0, 0, 0)
        
        # Nivel de corrección
        row1_col1 = QVBoxLayout()
        row1_col1.setSpacing(6)
        row1_col1.setContentsMargins(0, 0, 0, 0)
        label_correccion = QLabel("Nivel de corrección:")
        self.error_correction_combo = QComboBox()
        self.error_correction_combo.setMinimumWidth(120)
        self.error_correction_combo.setMaximumWidth(160)
        self.error_correction_combo.setMinimumHeight(32)
        self.error_correction_combo.addItems(['L (7%)', 'M (15%)', 'Q (25%)', 'H (30%)'])
        row1_col1.addWidget(label_correccion)
        row1_col1.addWidget(self.error_correction_combo)
        row1.addLayout(row1_col1)
        
        # Tamaño de caja
        row1_col2 = QVBoxLayout()
        row1_col2.setSpacing(6)
        row1_col2.setContentsMargins(0, 0, 0, 0)
        label_caja = QLabel("Tamaño de caja:")
        self.box_size_spin = QSpinBox()
        self.box_size_spin.setRange(1, 50)
        self.box_size_spin.setMinimumWidth(110)
        self.box_size_spin.setMaximumWidth(150)
        self.box_size_spin.setMinimumHeight(32)
        self.box_size_spin.setValue(10)
        row1_col2.addWidget(label_caja)
        row1_col2.addWidget(self.box_size_spin)
        row1.addLayout(row1_col2)
        
        # Borde
        row1_col3 = QVBoxLayout()
        row1_col3.setSpacing(6)
        row1_col3.setContentsMargins(0, 0, 0, 0)
        label_borde = QLabel("Borde:")
        self.border_spin = QSpinBox()
        self.border_spin.setRange(0, 20)
        self.border_spin.setMinimumWidth(110)
        self.border_spin.setMaximumWidth(150)
        self.border_spin.setMinimumHeight(32)
        self.border_spin.setValue(4)
        row1_col3.addWidget(label_borde)
        row1_col3.addWidget(self.border_spin)
        row1.addLayout(row1_col3)
        
        row1.addStretch()
        layout.addLayout(row1)
        
        # FILA 2: Versión, Color De Primer Plano, Color De Fondo
        row2 = QHBoxLayout()
        row2.setSpacing(50)
        row2.setContentsMargins(0, 0, 0, 0)
        
        # Versión
        row2_col1 = QVBoxLayout()
        row2_col1.setSpacing(6)
        row2_col1.setContentsMargins(0, 0, 0, 0)
        label_version = QLabel("Versión (Auto = 0):")
        self.version_spin = QSpinBox()
        self.version_spin.setRange(0, 40)
        self.version_spin.setMinimumWidth(110)
        self.version_spin.setMaximumWidth(150)
        self.version_spin.setMinimumHeight(32)
        self.version_spin.setValue(0)
        row2_col1.addWidget(label_version)
        row2_col1.addWidget(self.version_spin)
        row2.addLayout(row2_col1)
        
        # Color De Primer Plano
        row2_col2 = QVBoxLayout()
        row2_col2.setSpacing(6)
        row2_col2.setContentsMargins(0, 0, 0, 0)
        label_fg = QLabel("Color de primer plano:")
        self.color_fg_button = QPushButton("Seleccionar")
        self.color_fg_button.setMinimumWidth(100)
        self.color_fg_button.setMaximumWidth(140)
        self.color_fg_button.setMinimumHeight(32)
        self.color_fg_button.clicked.connect(lambda: self.seleccionar_color('fg'))
        row2_col2.addWidget(label_fg)
        row2_col2.addWidget(self.color_fg_button)
        row2.addLayout(row2_col2)
        
        # Color De Fondo
        row2_col3 = QVBoxLayout()
        row2_col3.setSpacing(6)
        row2_col3.setContentsMargins(0, 0, 0, 0)
        label_bg = QLabel("Color de fondo:")
        self.color_bg_button = QPushButton("Seleccionar")
        self.color_bg_button.setMinimumWidth(100)
        self.color_bg_button.setMaximumWidth(140)
        self.color_bg_button.setMinimumHeight(32)
        self.color_bg_button.clicked.connect(lambda: self.seleccionar_color('bg'))
        row2_col3.addWidget(label_bg)
        row2_col3.addWidget(self.color_bg_button)
        row2.addLayout(row2_col3)
        
        row2.addStretch()
        layout.addLayout(row2)
        
        # FILA 3: Agregar logo
        row3 = QHBoxLayout()
        row3.setSpacing(30)
        row3.setContentsMargins(0, 0, 0, 0)
        label_logo = QLabel("Agregar logo:")
        self.logo_check = QCheckBox("Usar Logo")
        row3.addWidget(label_logo)
        row3.addWidget(self.logo_check)
        row3.addStretch()
        layout.addLayout(row3)
        
        layout.addSpacing(10)
        
        # Botones en la misma fila - Centrados vertical y horizontalmente
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(20)
        buttons_row.setContentsMargins(0, 0, 0, 0)
        buttons_row.addStretch()
        
        self.logo_button = QPushButton("Seleccionar logo")
        self.logo_button.setMinimumWidth(140)
        self.logo_button.setMaximumWidth(160)
        self.logo_button.setMinimumHeight(36)
        self.logo_button.clicked.connect(self.seleccionar_logo)
        buttons_row.addWidget(self.logo_button)
        
        generar_personalizado = QPushButton("Generar QR personalizado")
        generar_personalizado.setMinimumWidth(180)
        generar_personalizado.setMaximumWidth(220)
        generar_personalizado.setMinimumHeight(36)
        generar_personalizado.clicked.connect(self.generar_qr_personalizado)
        buttons_row.addWidget(generar_personalizado)
        
        buttons_row.addStretch()
        layout.addLayout(buttons_row, 0)
        
        layout.addStretch(1)
        scroll_widget.setLayout(layout)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        widget.setLayout(main_layout)
        return widget

    def crear_tab_especiales(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10, 10, 10, 10)
        
        tabs_especiales = QTabWidget()
        
        # vCard
        vcard_widget = QWidget()
        vcard_layout = QVBoxLayout()
        vcard_layout.setSpacing(10)
        vcard_layout.setContentsMargins(8, 8, 8, 8)
        
        label_nombre = QLabel("Nombre:")
        label_nombre.setStyleSheet("font-size: 11px; min-width: 70px;")
        self.vcard_nombre = QLineEdit()
        self.vcard_nombre.setMinimumHeight(36)
        self.vcard_nombre.setMaximumHeight(36)
        nombre_layout = QHBoxLayout()
        nombre_layout.setContentsMargins(0, 0, 0, 0)
        nombre_layout.addWidget(label_nombre)
        nombre_layout.addWidget(self.vcard_nombre)
        vcard_layout.addLayout(nombre_layout)
        
        label_tel = QLabel("Teléfono:")
        label_tel.setStyleSheet("font-size: 11px; min-width: 70px;")
        self.vcard_telefono = QLineEdit()
        self.vcard_telefono.setMinimumHeight(36)
        self.vcard_telefono.setMaximumHeight(36)
        tel_layout = QHBoxLayout()
        tel_layout.setContentsMargins(0, 0, 0, 0)
        tel_layout.addWidget(label_tel)
        tel_layout.addWidget(self.vcard_telefono)
        vcard_layout.addLayout(tel_layout)
        
        label_email = QLabel("Email:")
        label_email.setStyleSheet("font-size: 11px; min-width: 70px;")
        self.vcard_email = QLineEdit()
        self.vcard_email.setMinimumHeight(36)
        self.vcard_email.setMaximumHeight(36)
        email_layout = QHBoxLayout()
        email_layout.setContentsMargins(0, 0, 0, 0)
        email_layout.addWidget(label_email)
        email_layout.addWidget(self.vcard_email)
        vcard_layout.addLayout(email_layout)
        
        label_org = QLabel("Organización:")
        label_org.setStyleSheet("font-size: 11px; min-width: 70px;")
        self.vcard_org = QLineEdit()
        self.vcard_org.setMinimumHeight(36)
        self.vcard_org.setMaximumHeight(36)
        org_layout = QHBoxLayout()
        org_layout.setContentsMargins(0, 0, 0, 0)
        org_layout.addWidget(label_org)
        org_layout.addWidget(self.vcard_org)
        vcard_layout.addLayout(org_layout)
        
        label_url = QLabel("URL:")
        label_url.setStyleSheet("font-size: 11px; min-width: 70px;")
        self.vcard_url = QLineEdit()
        self.vcard_url.setMinimumHeight(36)
        self.vcard_url.setMaximumHeight(36)
        url_layout = QHBoxLayout()
        url_layout.setContentsMargins(0, 0, 0, 0)
        url_layout.addWidget(label_url)
        url_layout.addWidget(self.vcard_url)
        vcard_layout.addLayout(url_layout)
        
        generar_vcard = QPushButton("Generar VCard")
        generar_vcard.setMinimumWidth(100)
        generar_vcard.setMaximumWidth(140)
        generar_vcard.setMinimumHeight(36)
        generar_vcard.setStyleSheet("text-align: center; padding: 0px;")
        generar_vcard.clicked.connect(self.generar_vcard_qr)
        vcard_layout.addSpacing(15)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(generar_vcard)
        button_layout.addStretch()
        vcard_layout.addLayout(button_layout)
        vcard_layout.addStretch()
        
        vcard_widget.setLayout(vcard_layout)
        tabs_especiales.addTab(vcard_widget, "vCard")
        
        # WiFi
        wifi_widget = QWidget()
        wifi_layout = QVBoxLayout()
        wifi_layout.setSpacing(10)
        wifi_layout.setContentsMargins(8, 8, 8, 8)
        
        label_ssid = QLabel("SSID:")
        label_ssid.setStyleSheet("font-size: 11px;")
        self.wifi_ssid = QLineEdit()
        self.wifi_ssid.setMinimumHeight(36)
        self.wifi_ssid.setMaximumHeight(36)
        wifi_layout.addWidget(label_ssid)
        wifi_layout.addWidget(self.wifi_ssid)
        
        label_pwd = QLabel("Contraseña:")
        label_pwd.setStyleSheet("font-size: 11px;")
        self.wifi_password = QLineEdit()
        self.wifi_password.setMinimumHeight(36)
        self.wifi_password.setMaximumHeight(36)
        self.wifi_password.setEchoMode(QLineEdit.EchoMode.Password)
        wifi_layout.addWidget(label_pwd)
        wifi_layout.addWidget(self.wifi_password)
        
        label_sec = QLabel("Seguridad:")
        label_sec.setStyleSheet("font-size: 11px;")
        self.wifi_security = QComboBox()
        self.wifi_security.setMinimumWidth(100)
        self.wifi_security.setMaximumWidth(140)
        self.wifi_security.setMinimumHeight(36)
        self.wifi_security.addItems(['WPA', 'WEP', 'nopass'])
        wifi_layout.addWidget(label_sec)
        wifi_layout.addWidget(self.wifi_security)
        
        self.wifi_hidden = QCheckBox("Red Oculta")
        wifi_layout.addWidget(self.wifi_hidden)
        
        generar_wifi = QPushButton("Generar WiFi")
        generar_wifi.setMinimumWidth(100)
        generar_wifi.setMaximumWidth(140)
        generar_wifi.setMinimumHeight(36)
        generar_wifi.clicked.connect(self.generar_wifi_qr)
        wifi_layout.addSpacing(15)
        button_layout_wifi = QHBoxLayout()
        button_layout_wifi.addStretch()
        button_layout_wifi.addWidget(generar_wifi)
        button_layout_wifi.addStretch()
        wifi_layout.addLayout(button_layout_wifi)
        wifi_layout.addStretch()
        
        wifi_widget.setLayout(wifi_layout)
        tabs_especiales.addTab(wifi_widget, "WiFi")
        
        # SMS
        sms_widget = QWidget()
        sms_layout = QVBoxLayout()
        sms_layout.setSpacing(10)
        sms_layout.setContentsMargins(8, 8, 8, 8)
        
        label_num = QLabel("Número:")
        label_num.setStyleSheet("font-size: 11px;")
        self.sms_numero = QLineEdit()
        self.sms_numero.setMinimumHeight(36)
        self.sms_numero.setMaximumHeight(36)
        sms_layout.addWidget(label_num)
        sms_layout.addWidget(self.sms_numero)
        
        label_msg = QLabel("Mensaje:")
        label_msg.setStyleSheet("font-size: 11px;")
        self.sms_mensaje = QTextEdit()
        self.sms_mensaje.setMinimumHeight(70)
        self.sms_mensaje.setMaximumHeight(90)
        sms_layout.addWidget(label_msg)
        sms_layout.addWidget(self.sms_mensaje)
        
        generar_sms = QPushButton("Generar SMS")
        generar_sms.setMinimumWidth(100)
        generar_sms.setMaximumWidth(140)
        generar_sms.setMinimumHeight(36)
        generar_sms.clicked.connect(self.generar_sms_qr)
        sms_layout.addSpacing(15)
        button_layout_sms = QHBoxLayout()
        button_layout_sms.addStretch()
        button_layout_sms.addWidget(generar_sms)
        button_layout_sms.addStretch()
        sms_layout.addLayout(button_layout_sms)
        sms_layout.addStretch()
        
        sms_widget.setLayout(sms_layout)
        tabs_especiales.addTab(sms_widget, "SMS")
        
        # Email
        email_widget = QWidget()
        email_layout = QVBoxLayout()
        email_layout.setSpacing(10)
        email_layout.setContentsMargins(8, 8, 8, 8)
        
        label_email = QLabel("Email:")
        label_email.setStyleSheet("font-size: 11px;")
        self.email_address = QLineEdit()
        self.email_address.setMinimumHeight(36)
        self.email_address.setMaximumHeight(36)
        email_layout.addWidget(label_email)
        email_layout.addWidget(self.email_address)
        
        label_subj = QLabel("Asunto:")
        label_subj.setStyleSheet("font-size: 11px;")
        self.email_subject = QLineEdit()
        self.email_subject.setMinimumHeight(36)
        self.email_subject.setMaximumHeight(36)
        email_layout.addWidget(label_subj)
        email_layout.addWidget(self.email_subject)
        
        label_body = QLabel("Cuerpo:")
        label_body.setStyleSheet("font-size: 11px;")
        self.email_body = QTextEdit()
        self.email_body.setMinimumHeight(60)
        self.email_body.setMaximumHeight(80)
        email_layout.addWidget(label_body)
        email_layout.addWidget(self.email_body)
        
        generar_email = QPushButton("Generar email")
        generar_email.setMinimumWidth(100)
        generar_email.setMaximumWidth(140)
        generar_email.setMinimumHeight(36)
        generar_email.clicked.connect(self.generar_email_qr)
        email_layout.addSpacing(15)
        button_layout_email = QHBoxLayout()
        button_layout_email.addStretch()
        button_layout_email.addWidget(generar_email)
        button_layout_email.addStretch()
        email_layout.addLayout(button_layout_email)
        email_layout.addStretch()
        
        email_widget.setLayout(email_layout)
        tabs_especiales.addTab(email_widget, "Email")
        
        layout.addWidget(tabs_especiales)
        layout.addSpacing(20)
        
        # Vista previa
        self.especiales_preview = QLabel()
        self.especiales_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.especiales_preview.setMinimumSize(350, 350)
        self.especiales_preview.setMaximumSize(350, 350)
        self.especiales_preview.setStyleSheet("border: 1px solid #cccccc;")
        preview_layout = QHBoxLayout()
        preview_layout.addStretch()
        preview_layout.addWidget(self.especiales_preview)
        preview_layout.addStretch()
        layout.addLayout(preview_layout)
        layout.addSpacing(8)
        
        # Estado
        self.especiales_status = QLabel()
        self.especiales_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.especiales_status)
        
        widget.setLayout(layout)
        return widget

    def crear_tab_lector(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Botón para cargar imagen - Centrado
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        cargar_button = QPushButton("Cargar imagen QR")
        cargar_button.setMinimumWidth(140)
        cargar_button.setMaximumWidth(170)
        cargar_button.setMinimumHeight(32)
        cargar_button.clicked.connect(self.cargar_imagen_lector)
        button_layout.addWidget(cargar_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        layout.addSpacing(25)
        
        # Preview de imagen cargada - Centrado
        self.lector_preview = QLabel()
        self.lector_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lector_preview.setMinimumSize(220, 220)
        self.lector_preview.setMaximumSize(300, 300)
        self.lector_preview.setStyleSheet("border: 1px solid #cccccc;")
        preview_layout = QHBoxLayout()
        preview_layout.addStretch()
        preview_layout.addWidget(self.lector_preview)
        preview_layout.addStretch()
        layout.addLayout(preview_layout)
        layout.addSpacing(25)
        
        # Resultado decodificado
        label_resultado = QLabel("Contenido decodificado:")
        label_resultado.setStyleSheet("font-weight: bold;")
        layout.addWidget(label_resultado)
        
        self.lector_resultado = QTextEdit()
        self.lector_resultado.setReadOnly(True)
        self.lector_resultado.setMinimumHeight(100)
        self.lector_resultado.setMaximumHeight(150)
        layout.addWidget(self.lector_resultado)
        
        # Estado
        self.lector_status = QLabel()
        self.lector_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lector_status)
        
        widget.setLayout(layout)
        return widget

    def crear_tab_historial(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Botones - Centrados
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        
        actualizar_button = QPushButton("Actualizar")
        actualizar_button.setMinimumWidth(110)
        actualizar_button.setMaximumWidth(140)
        actualizar_button.setMinimumHeight(32)
        actualizar_button.clicked.connect(self.actualizar_historial)
        
        limpiar_button = QPushButton("Limpiar historial")
        limpiar_button.setMinimumWidth(140)
        limpiar_button.setMaximumWidth(170)
        limpiar_button.setMinimumHeight(32)
        limpiar_button.clicked.connect(self.limpiar_historial_confirm)
        
        button_layout.addWidget(actualizar_button)
        button_layout.addWidget(limpiar_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Lista del historial
        self.historial_list = QListWidget()
        self.historial_list.itemClicked.connect(self.mostrar_detalles_historial)
        self.historial_list.setMinimumHeight(150)
        self.historial_list.setMaximumHeight(200)
        layout.addWidget(self.historial_list)
        
        # Detalles
        label_detalles = QLabel("Detalles:")
        label_detalles.setStyleSheet("font-weight: bold;")
        
        self.historial_detalles = QTextEdit()
        self.historial_detalles.setReadOnly(True)
        self.historial_detalles.setMinimumHeight(120)
        self.historial_detalles.setMaximumHeight(180)
        
        # Layout para juntar label y textarea sin espaciado
        detalles_layout = QVBoxLayout()
        detalles_layout.setSpacing(0)
        detalles_layout.setContentsMargins(0, 0, 0, 0)
        detalles_layout.addWidget(label_detalles)
        detalles_layout.addWidget(self.historial_detalles)
        layout.addLayout(detalles_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget

    # Métodos de funcionalidad
    
    def generar_qr_basico(self):
        texto = self.text_input.text().strip()
        if not texto:
            self.status_label.setText("⚠️ Ingrese un texto válido")
            return
        
        if self.validar_url_check.isChecked() and not self.generador.validar_url(texto):
            self.status_label.setText("⚠️ URL Inválida")
            return
        
        qr_path = self.generador.generar_vcard(texto, '', '', '', '')
        if qr_path:
            self.mostrar_preview(qr_path, self.qr_preview)
            self.status_label.setText("✓ QR generado exitosamente")
        else:
            self.status_label.setText("✗ Error al generar QR")

    def generar_qr_personalizado(self):
        texto = self.text_input.text().strip()
        if not texto:
            self.status_label.setText("⚠️ Ingrese un texto válido")
            return
        
        # Mapear nivel de corrección
        niveles_error = {0: qrcode.constants.ERROR_CORRECT_L,
                        1: qrcode.constants.ERROR_CORRECT_M,
                        2: qrcode.constants.ERROR_CORRECT_Q,
                        3: qrcode.constants.ERROR_CORRECT_H}
        
        config = {
            'error_correction': niveles_error[self.error_correction_combo.currentIndex()],
            'box_size': self.box_size_spin.value(),
            'border': self.border_spin.value(),
            'version': self.version_spin.value() if self.version_spin.value() > 0 else None,
            'fill_color': self.color_fg_value,
            'back_color': self.color_bg_value,
            'con_logo': self.logo_check.isChecked(),
            'logo_path': self.logo_path if hasattr(self, 'logo_path') else None
        }
        
        qr_path = self.generador.generar_codigo_qr(texto, **config)
        if qr_path:
            self.mostrar_preview(qr_path, self.qr_preview)
            self.status_label.setText("✓ QR personalizado generado")
        else:
            self.status_label.setText("✗ Error al generar QR")

    def guardar_qr(self):
        if not self.generador.codigo_qr:
            self.status_label.setText("⚠️ Genere un QR primero")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Código QR",
            "",
            f"{self.formato_combo.currentText()} Files (*.{self.formato_combo.currentText().lower()});;All Files (*)"
        )
        
        if filename:
            if self.generador.guardar_codigo_qr(filename, self.formato_combo.currentText()):
                self.status_label.setText(f"✓ Guardado en: {filename}")
            else:
                self.status_label.setText("✗ Error al guardar")

    def copiar_qr(self):
        if self.generador.copiar_al_portapapeles():
            self.status_label.setText("✓ QR copiado al portapapeles (Ruta Guardada)")
        else:
            self.status_label.setText("✗ Error al copiar")

    def seleccionar_color(self, tipo):
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            if tipo == 'fg':
                self.color_fg_value = hex_color
                self.color_fg_button.setStyleSheet(f"background-color: {hex_color}; color: white;")
            else:
                self.color_bg_value = hex_color
                self.color_bg_button.setStyleSheet(f"background-color: {hex_color}; border: 1px solid black;")

    def seleccionar_logo(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Logo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        if filename:
            self.logo_path = filename
            self.logo_button.setText(f"Logo: {os.path.basename(filename)}")

    def generar_vcard_qr(self):
        nombre = self.vcard_nombre.text().strip()
        if not nombre:
            self.especiales_status.setText("⚠️ Ingrese un nombre")
            return
        
        qr_path = self.generador.generar_vcard(
            nombre,
            self.vcard_telefono.text(),
            self.vcard_email.text(),
            self.vcard_org.text(),
            self.vcard_url.text()
        )
        
        if qr_path:
            self.mostrar_preview(qr_path, self.especiales_preview)
            self.especiales_status.setText("✓ vCard QR generada")
        else:
            self.especiales_status.setText("✗ Error")

    def generar_wifi_qr(self):
        ssid = self.wifi_ssid.text().strip()
        password = self.wifi_password.text()
        
        if not ssid:
            self.especiales_status.setText("⚠️ Ingrese SSID")
            return
        
        qr_path = self.generador.generar_wifi(
            ssid,
            password,
            self.wifi_security.currentText(),
            self.wifi_hidden.isChecked()
        )
        
        if qr_path:
            self.mostrar_preview(qr_path, self.especiales_preview)
            self.especiales_status.setText("✓ WiFi QR generada")

    def generar_sms_qr(self):
        numero = self.sms_numero.text().strip()
        if not numero:
            self.especiales_status.setText("⚠️ Ingrese un número")
            return
        
        qr_path = self.generador.generar_sms(numero, self.sms_mensaje.toPlainText())
        
        if qr_path:
            self.mostrar_preview(qr_path, self.especiales_preview)
            self.especiales_status.setText("✓ SMS QR generada")

    def generar_email_qr(self):
        email = self.email_address.text().strip()
        if not email:
            self.especiales_status.setText("⚠️ Ingrese un email")
            return
        
        qr_path = self.generador.generar_email(
            email,
            self.email_subject.text(),
            self.email_body.toPlainText()
        )
        
        if qr_path:
            self.mostrar_preview(qr_path, self.especiales_preview)
            self.especiales_status.setText("✓ Email QR generada")

    def cargar_imagen_lector(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Cargar Imagen QR",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        
        if filename:
            self.mostrar_preview(filename, self.lector_preview)
            
            textos, estado = self.generador.decodificar_qr(filename)
            
            if textos:
                self.lector_resultado.setText("\n".join(textos))
                self.lector_status.setText("✓ QR decodificado exitosamente")
            else:
                self.lector_resultado.setText(estado)
                self.lector_status.setText(f"✗ {estado}")

    def actualizar_historial(self):
        self.historial_list.clear()
        historial = self.generador.obtener_historial()
        
        for entrada in historial:
            item = QListWidgetItem(f"{entrada['texto'][:50]}... ({entrada['timestamp'][:10]})")
            self.historial_list.addItem(item)

    def mostrar_detalles_historial(self, item):
        historial = self.generador.obtener_historial()
        index = self.historial_list.row(item)
        
        if 0 <= index < len(historial):
            entrada = historial[index]
            detalles = f"Texto: {entrada['texto']}\n\n"
            detalles += f"Timestamp: {entrada['timestamp']}\n\n"
            detalles += f"Configuración:\n{json.dumps(entrada['config'], indent=2, default=str)}"
            self.historial_detalles.setText(detalles)

    def limpiar_historial_confirm(self):
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "¿Está seguro de que desea limpiar el historial?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.generador.limpiar_historial()
            self.historial_list.clear()
            self.historial_detalles.clear()

    def actualizar_estadisticas(self):
        texto = self.text_input.text()
        stats = self.generador.obtener_estadisticas(texto)
        self.stats_label.setText(
            f"Caracteres: {stats['caracteres']} | "
            f"Palabras: {stats['palabras']} | "
            f"Líneas: {stats['lineas']}"
        )
        
        if self.validar_url_check.isChecked() and texto:
            if self.generador.validar_url(texto):
                self.url_status_label.setText("✓ URL Válida")
                self.url_status_label.setStyleSheet("color: green;")
            else:
                self.url_status_label.setText("✗ URL Inválida")
                self.url_status_label.setStyleSheet("color: red;")

    def mostrar_preview(self, ruta, label):
        pixmap = QPixmap(ruta)
        scaled = pixmap.scaledToWidth(330, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(scaled)

    def aplicar_estilo(self):
        if self.tema_oscuro:
            self.setStyleSheet(ESTILO_OSCURO)
        else:
            self.setStyleSheet(ESTILO_CLARO)
    
    def cambiar_tema(self):
        """Alterna entre tema oscuro y claro"""
        self.tema_oscuro = not self.tema_oscuro
        self.aplicar_estilo()
        if self.tema_oscuro:
            self.boton_tema.setText("☀️")
        else:
            self.boton_tema.setText("🌙")

    # Color inicial
    color_fg_value = 'black'
    color_bg_value = 'white'


def main():
    import json  # Agregar en imports
    app = QApplication(sys.argv)
    ex = InterfazQR()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
