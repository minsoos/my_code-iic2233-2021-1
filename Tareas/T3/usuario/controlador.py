from ventanas.ventana_inicio import VentanaInicio
from ventanas.ventana_espera import VentanaEspera
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from utils import cargar_parametros, normalizar_ruta


class Controlador(QObject):

    senal_enviar_mensaje = pyqtSignal(object)
    senal_respuesta_ingreso_sala_espera = pyqtSignal(bool, str)
    senal_abrir_ventana_espera = pyqtSignal(str, int)

    def __init__(self, ruta_logo, ruta_nubes) -> None:
        super().__init__()
        self.ventana_inicio = VentanaInicio(ruta_logo, ruta_nubes)
        self.ventana_espera = VentanaEspera()

        self.dict_jugadores_activos = dict()

        self.conexiones()

    def conexiones(self):
        self.ventana_inicio.senal_intentar_ingreso.connect(self.intentar_ingreso_sala_espera)
        self.senal_respuesta_ingreso_sala_espera.connect(self.ventana_inicio.tramitar_ingreso)

        self.senal_abrir_ventana_espera.connect(self.ventana_espera.inicializar_usuario)
        self.ventana_espera.senal_iniciar_juego.connect(self.iniciar_juego)
        self.ventana_espera.senal_votar.connect(self.votar_mapa)

    def intentar_ingreso_sala_espera(self, nombre):
        diccionario = {
            "comando": "intentar ingreso sala de espera",
            "nombre": nombre
        }
        self.enviar_mensaje_a_servidor(diccionario)

    def enviar_mensaje_a_servidor(self, diccionario):
        self.senal_enviar_mensaje.emit(diccionario)

    def manejar_mensaje(self, mensaje):
        accion = mensaje["comando"]

        if accion == "ingreso aceptado":
            self.aceptar_usuario_a_espera(mensaje["nombre"], mensaje["color usuario"])
            
        elif accion == "ingreso denegado":
            causal = mensaje["causal"]
            if causal == "cupos":
                self.senal_respuesta_ingreso_sala_espera.emit(False, "cupos")
            elif causal == "nombre":
                self.senal_respuesta_ingreso_sala_espera.emit(False, "nombre")
            else:
                raise ValueError("La causal no se encuentra en mis registros")
        else:
            raise ValueError("La acción no está en mis registros")
    
    def aceptar_usuario_a_espera(self, nombre, n_color):
        self.nombre_usuario = nombre
        self.int_color_usuario = n_color
        self.senal_respuesta_ingreso_sala_espera.emit(True, "True")
        self.senal_abrir_ventana_espera.emit(nombre, n_color)
        self.dict_jugadores_activos[n_color] = nombre

    def mostrar_login(self):
        pass

    # ---------------------------------- Sala de espera

    def iniciar_juego(self):
        diccionario = {
            "comando": "iniciar juego"
        }
        self.enviar_mensaje_a_servidor(diccionario)
    
    def votar_mapa(self, mapa):
        diccionario = {
            "comando": "votar",
            "voto": mapa
        }
        self.enviar_mensaje_a_servidor(diccionario)