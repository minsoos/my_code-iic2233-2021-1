import os
import sys
from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout,
    QVBoxLayout, QPushButton, QApplication,
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap


class VentanaInicio(QWidget):
    """
    Ventana de log-in para el juego. Consta de una imagen, un campo de texto y un boton para
    ingresar. Es la primera ventana que se ve en el programa
    """
    senal_abrir_eleccion_personaje = pyqtSignal(str)  # Señal que abre la ventana de eleccion
    senal_elegir_nombre = pyqtSignal(str)  # Señal para enviar el nombre al back-end para verificar

    def __init__(self, ancho=400, alto=400, ruta_logo=os.path.join("assets", "logo.jpg")):
        # NO MODIFICAR
        super().__init__()
        self.size = (ancho, alto)
        self.resize(ancho, alto)

        self.setWindowTitle("Ventana Inicio")
        self.init_gui(ruta_logo)  # Llamada a la funcion que inicia la interfaz

    def init_gui(self, ruta_logo):
        self.imagen = QLabel(self)
        self.imagen.setGeometry(300, 300, 300, 300)
        pixeles = QPixmap(ruta_logo)
        self.imagen.setPixmap(pixeles)
        self.imagen.resize(self.imagen.sizeHint())
        self.imagen.setScaledContents(True)
        #
        self.line_edit_nombre = QLineEdit("", self)
        #
        self.label_explicativo = QLabel("Ingrese su nombre", self)
        #
        self.boton = QPushButton("Entrar", self)
        self.boton.clicked.connect(self.enviar_nombre)
        #
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.imagen)
        layout.addWidget(self.line_edit_nombre)
        layout.addWidget(self.label_explicativo)
        layout.addWidget(self.boton)
        layout.addStretch()
        self.setLayout(layout)
        #
        self.show()
    def enviar_nombre(self):
        self.senal_elegir_nombre.emit(self.line_edit_nombre.text())
        pass

    def recibir_validacion(self, validado):
        # NO MODIFICAR
        """
        Este método recibe desde el back-end una señal que indica si el nombre enviado es
        valido o no. De ser valido, se sigue a la siguiente ventana. En el caso contrario, se borra
        el texto del QLine y se notifica que el nombre es invalido
        """
        if validado:
            self.hide()
            self.senal_abrir_eleccion_personaje.emit(self.line_edit_nombre.text())
        else:
            self.line_edit_nombre.clear()
            self.line_edit_nombre.setPlaceholderText("Nombre inválido")

if __name__ == "__main__":
    app = QApplication([])
    jeje = VentanaInicio()
    sys.exit(app.exec())