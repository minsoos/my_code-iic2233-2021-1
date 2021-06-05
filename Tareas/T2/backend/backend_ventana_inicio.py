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
from backend.personajes import Gorgory, Homero, Lisa, Moe, Krusty
from random import randint


class LogicaVentanaInicio(QObject):

    senal_inicio_partida = pyqtSignal(str)
    senal_ventana_error = pyqtSignal()
    senal_ventana_ranking = pyqtSignal()

    def __init__(self):
        '''
        Back-end de la ventana ventana inicio, esta comprueba
        que el nombre de usuario cumpla con la restricción. En
        el caso positivo, cierra ventana inicio, y abre ventana de
        preparación. De lo contrario, abre un message de error
        '''
        super().__init__()

    def comprobar_alfanum(self, usuario) -> bool:
        '''
        Recibe la senal_iniciar_partida y
        Comprueba que lo ingresado en el QLineEdit es correcto
        '''
        if usuario.isalnum():
            self.ingreso_correcto(usuario)
            #Crear partida
        else:
            self.mensaje_error()
    
    def ingreso_correcto(self, usuario) -> None:
        '''
        Envia la senal senal_inicio_partida a
        el frontend de VentanaInicio, para cerrar la ventana inicio,
        y a VentanaPreparacion para abrir la ventana de preparación
        '''
        self.senal_inicio_partida.emit(usuario)

    def mensaje_error(self) -> None:
        '''
        Abre el mensaje de error
        '''
        self.senal_ventana_error.emit()

    def requerimiento_ver_ranking(self) -> None:
        '''
        Abre la ventana de ranking mediante la señal
        senal_abrir_ranking
        '''
        self.senal_ventana_ranking.emit()
