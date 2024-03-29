from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

import parametros as p


window_name_main, base_class_main = uic.loadUiType(p.VENTANA_INICIO)
window_name_error, base_class_error = uic.loadUiType(p.VENTANA_ERROR)


class VentanaInicio(window_name_main, base_class_main):
    # DEBES MODIFICAR ESTA CLASE
    #unir esta señal al backend en el main.py
    senal_verificar_usuario = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #setea el logo
        self.logo.setPixmap(QPixmap(p.LOGO_INICIO))
        #Escala el contenido de acuerdo con el label logo
        self.logo.setScaledContents(True)
        #Le pone un background transparente al fondo blanco
        self.logo.setAttribute(Qt.WA_TranslucentBackground)
        #Setea el fondo en el label fondo
        self.fondo.setPixmap(QPixmap(p.FONDO))
        self.fondo.setScaledContents(True)
        

        # PUEDES MODIFICAR DESDE ESTA LÍNEA
        self.boton_comenzar.clicked.connect(self.verificar_usuario)
        self.boton_salir.clicked.connect(self.salir)

        # HASTA AQUI
        self.show()

    def verificar_usuario(self):
        self.senal_verificar_usuario.emit(self.campo_nombre.text())

    def salir(self):
        # NO MODIFICAR
        self.close()

    def mostrar_ventana(self):
        # NO MODIFICAR
        self.campo_nombre.setText("")
        self.show()


class VentanaError(window_name_error, base_class_error):
    # NO DEBES MODIFICAR ESTA CLASE

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_volver.clicked.connect(self.esconder)
        self.logo.setPixmap(QPixmap(p.IMAGEN_ERROR))
        self.logo.setScaledContents(True)

    def mostrar(self):
        self.show()

    def esconder(self):
        self.hide()
