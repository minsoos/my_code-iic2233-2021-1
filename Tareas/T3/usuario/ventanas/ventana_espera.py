from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from utils import cargar_parametros, normalizar_ruta

parametros = cargar_parametros("parametros.json")
path_ventana_espera = parametros["RUTAS"]["VENTANA_ESPERA"]
path_ventana_espera = normalizar_ruta(path_ventana_espera)
nombre, padre = uic.loadUiType(path_ventana_espera)


class VentanaEspera(nombre, padre):

    senal_iniciar_juego = pyqtSignal()
    senal_votar = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.voto = False
        self.posiciones_jugadores = dict()

        parametros = cargar_parametros()
        dict_parametros = dict()
        mapa_sj = parametros["RUTAS"]["MAPA_SAN_JOAQUIN"]
        dict_parametros["mapa_sj"] = mapa_sj
        mapa_ing = parametros["RUTAS"]["MAPA_INGENIERIA"]
        dict_parametros["mapa_ing"] = mapa_ing
        fondo = parametros["RUTAS"]["IMAGEN_NUBES_ESPERA"]
        dict_parametros["fondo"] = fondo
        for elemento in dict_parametros:
            dict_parametros[elemento] = normalizar_ruta(dict_parametros[elemento])
        
        self.mapa_ingenieria.setPixmap(QPixmap(dict_parametros["mapa_ing"]))
        self.mapa_san_joaquin.setPixmap(QPixmap(dict_parametros["mapa_sj"]))
        self.label_fondo.setPixmap(QPixmap(dict_parametros["fondo"]))

        self.boton_iniciar.clicked.connect(self.metodo_iniciar)
        self.boton_votar.clicked.connect(self.metodo_votar)

        self.labels_jugadores = dict()
        i = 1
        for jugador in (self.label_nombre_jugador1, self.label_nombre_jugador2,\
            self.label_nombre_jugador3, self.label_nombre_jugador4):

            self.labels_jugadores[i] = jugador
            i += 1
        
        self.labels_estados_jugadores = dict()
        i = 1
        for jugador in (self.label_estado_jugador1, self.label_estado_jugador2,\
            self.label_estado_jugador3, self.label_estado_jugador4):

            self.labels_estados_jugadores[i] = jugador
            i += 1

        self.boton_iniciar.hide()

    def mostrar(self):
        self.show()
    
    def esconderse(self):
        self.hide()

    def inicializar_usuario(self, nombre, n_color, eres_jefe):
        if eres_jefe:
            self.boton_iniciar.show()
            self.boton_iniciar.setEnabled(True)
        self.posiciones_jugadores[nombre] = n_color
        self.labels_jugadores[n_color].setText(nombre)
        self.mostrar()

    def metodo_votar(self):
        if not self.voto:
            if self.boton_ingenieria.isChecked():
                self.senal_votar.emit("ingenieria")
                self.voto = True
            elif self.boton_san_joaquin.isChecked():
                self.senal_votar.emit("san joaquin")
                self.voto = True

    def actualizar_votos(self, nombres_votadores, votos_sj, votos_ing):

        self.votos_ingenieria.setText(str(votos_ing))
        self.votos_san_joaquin.setText(str(votos_sj))

        for nombre_votador in nombres_votadores:
            numero = self.posiciones_jugadores[nombre_votador]
            label = self.labels_estados_jugadores[numero]
            label.setText("LISTO")
            label.setStyleSheet("color: rgb(0, 255, 0)")

    def nuevo_usuario(self, nombre, n_color):
        self.posiciones_jugadores[nombre] = n_color
        self.labels_jugadores[n_color].setText(nombre)

    def metodo_iniciar(self):
        if self.voto:
            self.senal_iniciar_juego.emit()

    def limpiar_sala(self):
        for numero in self.posiciones_jugadores.values():
            label = self.labels_estados_jugadores[numero]
            label.setText("DESCONECTADO")
            label.setStyleSheet("color: rgb(255, 0, 0)")
        
        self.votos_ingenieria.setText(str(0))
        self.votos_san_joaquin.setText(str(0))
        self.voto = False
