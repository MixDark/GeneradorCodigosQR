import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from Codigo_QR import GeneradorCodigoQR

class InterfazQR(QMainWindow, GeneradorCodigoQR):
    def __init__(self):
        super().__init__()
        GeneradorCodigoQR.__init__(self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Generador de códigos QR')
        self.setFixedSize(500, 400)
        self.setWindowIcon(QIcon('icono.png'))
        
        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)  # Aumenta el espacio vertical entre widgets
        layout.setContentsMargins(20, 20, 20, 20)  # Añade márgenes
        
        # Estilo CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-family: Arial;
                font-size: 12px;
                font-weight: bold;
                color: #333333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
                color: black;
                font-size: 12px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)

        # Elementos de la interfaz
        label = QLabel("Ingrese el texto o la URL")
        self.text_input = QLineEdit()
        
        # Layout para botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(80)  # Espacio entre botones
                
        self.generate_button = QPushButton("Generar")
        self.save_button = QPushButton("Guardar")
        self.save_button.setEnabled(False)

        # Añadir espacio flexible antes de los botones
        button_layout.addStretch()
                
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.save_button)

        # Añadir espacio flexible después de los botones
        button_layout.addStretch()
        
        # Layout para el QR
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setMinimumSize(200, 200)
        
        # Mensaje de estado
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Agregar widgets al layout principal
        layout.addWidget(label)
        layout.addWidget(self.text_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.qr_label)
        layout.addWidget(self.status_label)
        layout.addStretch()  # Añade espacio flexible al final
        
        # Conectar señales
        self.generate_button.clicked.connect(self.generar_qr)
        self.save_button.clicked.connect(self.guardar_qr)

    def generar_qr(self):
        texto = self.text_input.text()
        if texto:
            # Generar el código QR
            qr_path = self.generar_codigo_qr(texto)
            
            if qr_path and os.path.exists(qr_path):
                # Mostrar el QR en la interfaz
                pixmap = QPixmap(qr_path)
                scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.qr_label.setPixmap(scaled_pixmap)
                
                self.save_button.setEnabled(True)
                self.status_label.setText("Generado exitosamente")
            else:
                self.save_button.setEnabled(False)
                self.status_label.setText("Error al generar el código QR")
        else:
            self.status_label.setText("Por favor ingrese un texto o URL")
            self.save_button.setEnabled(False)

    def guardar_qr(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Código QR",
            "",
            "PNG Files (*.png);;All Files (*)"
        )
        if filename:
            if self.guardar_codigo_qr(filename):
                self.status_label.setText("Guardado exitosamente")
            else:
                self.status_label.setText("Error al guardar el código QR")

def main():
    app = QApplication(sys.argv)
    ex = InterfazQR()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
