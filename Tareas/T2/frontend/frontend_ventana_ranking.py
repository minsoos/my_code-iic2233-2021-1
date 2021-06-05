from PyQt5 import uic
import parametros as p
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QEventLoop, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QLineEdit, QRadioButton, QSpinBox, QCheckBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
import sys
import parametros as p
from os import path
from random import randint

nombre, padre = uic.loadUiType(p.DISENO_VENTANA_RANKING)


class VentanaRanking(nombre, padre):

    senal_pedir_actualizar = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ventana de Ranking")
        '''
        Front-end de la ventana mostrando los 5 mejores
        puntajes del juego
        '''
        #Label de título
        #Formulario de 5 label
        #QPushButton para volver
        self.boton_volver.clicked.connect(self.solicitud_volver)
        self.puntajes_top = {
            1: self.puntaje1,
            2: self.puntaje2,
            3: self.puntaje3,
            4: self.puntaje4,
            5: self.puntaje5,
        }
        self.usuarios_top = {
            1: self.usuario1,
            2: self.usuario2,
            3: self.usuario3,
            4: self.usuario4,
            5: self.usuario5,
        }
        self.label_logo.setPixmap(QPixmap(p.RUTA_LOGO_RANKING))
    
    def solicitud_volver(self) -> None:
        '''
        Método conectado al QPushButton volver, cierra
        la ventana de ranking
        '''
        self.hide()
    
    def mostrar(self):
        self.senal_pedir_actualizar.emit()
        self.show()

    def actualizar(self, lista):
        for i in range(len(lista)):
            if i > 4:
                break
            self.usuarios_top[i+1].setText(lista[i][0])
            self.puntajes_top[i+1].setText(f"{lista[i][1]} ptos.")