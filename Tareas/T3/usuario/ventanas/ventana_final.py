from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMovie, QPen, QPixmap, QIcon, QPainter
from PyQt5 import uic
from PyQt5.QtWidgets import QLabel
from utils import (cargar_parametros, normalizar_ruta, ordenamiento_por_puntaje)
from collections import deque
parametros = cargar_parametros("parametros.json")
path_ventana_espera = parametros["RUTAS"]["VENTANA_FINAL"]
path_ventana_espera = normalizar_ruta(path_ventana_espera)
nombre, padre = uic.loadUiType(path_ventana_espera)


class VentanaFinal(nombre, padre):

    senal_jugar_denuevo = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.nombres_segun_puestos = {
            "1": self.nombre_puesto_1,
            "2": self.nombre_puesto_2,
            "3": self.nombre_puesto_3,
            "4": self.nombre_puesto_4
        }

        self.puntajes_segun_puestos = {
            "1": self.puntos_puesto_1,
            "2": self.puntos_puesto_2,
            "3": self.puntos_puesto_3,
            "4": self.puntos_puesto_4
        }
        parametros = cargar_parametros("parametros.json")
        self.boton_jugar_denuevo.clicked.connect(self.metodo_jugar_denuevo)
        ruta_fondo = normalizar_ruta(parametros["RUTAS"]["IMAGEN_NUBES_ESPERA"])
        self.label_fondo_nubes.setPixmap(QPixmap(ruta_fondo))
        ruta_gif = normalizar_ruta(parametros["RUTAS"]["GIF_CELEBRACION"])
        #        https://pythonpyqt.com/pyqt-gif/
        self.movie = QMovie(ruta_gif)
        self.label_gif.setMovie(self.movie)
        self.movie.start()
        self.label_gif.hide()

    def mostrar(self):
        self.show()

    def ocultar(self):
        self.hide()

    def limpiar_ventana(self):
        for puesto in self.nombres_segun_puestos:
            self.nombres_segun_puestos[puesto].setText("None")
        for puesto in self.puntajes_segun_puestos:
            self.puntajes_segun_puestos[puesto].setText("0")
        self.label_gif.hide()

    def ingresar_puntajes_y_usuarios(self, lista_jugadores):
        cola = deque(lista_jugadores)
        print("lista jugadores",lista_jugadores)
        i = 1
        while len(cola) > 0:
            jugador = cola.popleft()
            self.nombres_segun_puestos[str(i)].setText(str(jugador[0]))
            self.puntajes_segun_puestos[str(i)].setText(str(jugador[1]))
            i += 1
        
        self.mostrar()

    def metodo_jugar_denuevo(self):
        self.senal_jugar_denuevo.emit()
        self.limpiar_ventana()
        self.ocultar()
    
    def habilitar_gif_celebracion(self):
        self.label_gif.show()
        