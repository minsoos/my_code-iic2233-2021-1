from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QEventLoop, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QLineEdit, QRadioButton, QSpinBox, QCheckBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
import sys
import parametros as p
from personajes import Personaje, Homero, Lisa, Moe, Gorgory, Krusty
from os import path
from random import randint
from PyQt5 import uic
import funciones as f

nombre, padre = uic.loadUiType(p.DISENO_VENTANA_POSTRONDA)


class VentanaPostRonda(nombre, padre):

    senal_salir = pyqtSignal()
    senal_continuar = pyqtSignal()
    senal_salir_inicio = pyqtSignal()


    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        '''
        Esta ventana contendrá la información del juego que acaba
        de ocurrir, podrá elegir salir a la ventana de inicio o
        continuar jugando, e ir a la ventana de preparación
        '''
        self.label_foto.setPixmap(QPixmap(p.RUTA_FOTO_POSTRONDA))
        self.boton_salir.clicked.connect(self.metodo_salir)
        self.boton_salir_inicio.clicked.connect(self.metodo_salir_inicio)
        self.boton_continuar.clicked.connect(self.metodo_continuar)
    
    def inicializar_ventana(self, puntaje, i_buenos, i_malos, vida, perdio):
        self.label_puntaje.setText(f"{puntaje}")
        self.label_items_buenos.setText(f"{i_buenos}")
        self.label_items_malos.setText(f"{i_malos}")
        self.label_vida.setText(f"{vida}")
        self.boton_continuar.setEnabled(not perdio)
        if perdio:
            self.label_perdio.show()
            self.label_no_perdio.hide()
        else:
            self.label_no_perdio.show()
            self.label_perdio.hide()
        self.show()
    
    def metodo_salir(self):
        self.hide()
        self.senal_salir.emit()
    
    def metodo_salir_inicio(self):
        self.hide()
        self.senal_salir_inicio.emit()
    
    def metodo_continuar(self):
        self.hide()
        self.senal_continuar.emit()


class LogicaVentanaPostRonda(QObject):

    senal_inicializar = pyqtSignal(int, int, int, int, bool)
    senal_abrir_inicio = pyqtSignal()
    senal_volver_preparacion = pyqtSignal(int, int, int)
    senal_guardar_progreso = pyqtSignal(int, int, int)

    def __init__(self) -> None:
        super().__init__()
        '''
        Este es el backend de la ventana post ronda
        '''

    def salir(self):
        '''
        Te saca del programa
        '''
        self.guardar_progreso()
        QApplication.quit()

    def salir_a_inicio(self):
        '''
        Te lleva a la ventana de inicio y cierra la actual
        '''
        self.guardar_progreso()
        self.senal_abrir_inicio.emit()
        

    def continuar_juego(self):
        '''
        Te lleva a la ventana de preparación y cierra la actual
        '''
        self.senal_volver_preparacion.emit(self.puntaje, self.i_buenos, self.i_malos)
    
    def guardar_progreso(self):
        self.senal_guardar_progreso.emit(self.puntaje, self.i_buenos, self.i_malos)
    
    def inicializar_ventana(self, puntaje, i_buenos, i_malos, vida):
        vida = vida * 100
        self.vida = vida
        self.puntaje = puntaje
        self.i_buenos = i_buenos
        self.i_malos = i_malos
        if vida > 0:
            perdio = False
        else:
            perdio = True
        self.senal_inicializar.emit(puntaje, i_buenos, i_malos, vida, perdio)