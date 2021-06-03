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
from personajes import Gorgory, Homero, Lisa, Moe, Krusty
from os import path
from random import randint
import funciones as f

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


class FormularioPodio():

    senal_pedir_ranking = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        '''
        Ventana mostrando los 5 mejores puntajes
        del juego
        '''
        #5 Labels en un layout
        #llama a pedir_ranking

    def pedir_ranking(self) -> None:
        '''
        Usa la senal_pedir_ranking para indicar a
        la lógica que cargue el ranking
        '''

    def recibir_ranking(self, lista_ranking) -> None:
        '''
        Recibe la senal_cargar_formulario para setear
        los label del formulario
        '''


class LogicaVentanaRanking(QObject):

    senal_cargar_puntajes = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        '''
        back-end de la ventana ranking, se encarga de
        leer el archivo txt y llenar los qlabels de esta
        '''
    def extraer_lugares(self) -> list:
        '''
        lee el archivo en la ruta RUTA_RANKING, que contiene
        los puntajes de los mejores puntajes y sus usuarios
        retorna una lista de tuples, que contienen los puntajes
        y usuarios de los mejores jugadores. La posición n de la 
        lista corresponde a la n+1 en el ranking 
        '''
        with open(p.RUTA_RANKING, encoding="UTF-8") as archivo:
            lista = archivo.readlines()
            lista = map(lambda x: list(x.strip().split(",")), lista)
            lista = list(map(lambda x: (x[0], int(x[1])), lista))
        lista.sort(key=f.ordenar_por_puntaje, reverse=True)
        self.cargar_lugares(lista)

    def cargar_lugares(self, lista) -> None:
        '''
        extrae los lugares desde extraer lugares, y los envía
        mediante senal_cargar_formulario al formulario, para llenar
        los labels, si hay menos de 5 puntajes, se llena hasta las 5
        posiciones con ("Jugador malo", 0)
        '''
        self.senal_cargar_puntajes.emit(lista)