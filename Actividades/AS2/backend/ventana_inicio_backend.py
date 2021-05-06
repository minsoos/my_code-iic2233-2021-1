import os
import sys

from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication


class VentanaInicioBackend(QObject):

    senal_empezar_juego = pyqtSignal(str)
    senal_mensaje_error = pyqtSignal()

    def __init__(self, ruta_cancion):
        # NO MODIFICAR ESTE MÉTODO
        super().__init__()
        self.musica = Musica(ruta_cancion)
        self.start()
    
    def verificar_usuario(self, usuario):
        if "," not in usuario and usuario != "":
            self.senal_empezar_juego.emit(usuario)
        else:
            self.senal_mensaje_error.emit()           

    def start(self):
        # NO MODIFICAR ESTE MÉTODO
        self.musica.comenzar()



class Musica(QObject):
    # NO MODIFICAR ESTA CLASE

    def __init__(self, ruta_cancion):
        super().__init__()
        self.ruta_cancion = ruta_cancion

    def comenzar(self):
        try:
            self.cancion = QtMultimedia.QSound(self.ruta_cancion)
            self.cancion.Loop()
            self.cancion.play()
        except Exception as error:
            print('No se pudo iniciar la cancion', error)