import parametros as p
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QObject, QTime, pyqtSignal, QTimer, QEventLoop, Qt
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


class Musica(QObject):
    # Base de actividad AS2

    def __init__(self):
        super().__init__()
        self.ruta_cancion = p.RUTA_MUSICA
        self.timer = QTimer()
        self.timer.setInterval(1000*128)
        self.timer.timeout.connect(self.comenzar)
        self.comenzar()
        self.timer.start()

    def comenzar(self):
        try:
            self.cancion = QtMultimedia.QSound(self.ruta_cancion)
            self.cancion.Loop()
            self.cancion.play()
        except Exception as error:
            print('No se pudo iniciar la cancion', error)