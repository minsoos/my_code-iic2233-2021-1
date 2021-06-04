import parametros as p
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QObject, QThread, QTime, pyqtSignal, QTimer, QEventLoop, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QLineEdit, QRadioButton, QSpinBox, QCheckBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
import sys
from personajes import Personaje, Homero, Lisa, Moe, Gorgory, Krusty
from os import path
from random import randint
from PyQt5 import uic
import funciones as f
from ventana_postronda import VentanaPostRonda, LogicaVentanaPostRonda
from time import time
from collections import deque
from PyQt5 import QtCore, QtMultimedia


class Musica(QThread):
    # Base de actividad AS2

    def __init__(self):
        super().__init__()
        self.ruta_cancion = p.RUTA_MUSICA
        # self.timer = QTimer()
        # self.timer.setInterval(1000*128)
        # self.timer.timeout.connect(self.comenzar)
        # self.comenzar()
        # self.timer.start()
        self.empezar()
        self.pausado = False

    def empezar(self, *args, **kwargs):
        self.cancion = QtMultimedia.QSound(self.ruta_cancion)
        self.cancion.setLoops(-1)
        # Fuente: https://www.programmersought.com/article/37923092494/
        self.cancion.play()
    
    def pausar(self):
        if self.pausado:
            self.pausado = False
            self.cancion.play()
        else:
            self.pausado = True
            self.cancion.stop()