from ventanas.ventana_inicio import VentanaInicio
from ventanas.ventana_espera import VentanaEspera
from ventanas.ventana_juego import VentanaJuego
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from utils import cargar_parametros, normalizar_ruta


class Controlador(QObject):

    # Hacia el usuario.py
    senal_enviar_mensaje = pyqtSignal(object)
    # Hacia la sala de espera
    senal_respuesta_ingreso_sala_espera = pyqtSignal(bool, str)
    senal_abrir_ventana_espera = pyqtSignal(str, int, bool)
    senal_actualizar_votos = pyqtSignal(list, int, int)
    senal_nuevo_usuario = pyqtSignal(str, int)
    # Hacia la ventana juego
    senal_inicializar_jugadores_en_juego = pyqtSignal(list)
    senal_inscribir_jugador_en_juego = pyqtSignal(str)
    senal_enviar_imagen_a_juego = pyqtSignal(bytearray, int)
    senal_definir_mapa_en_juego = pyqtSignal(str)
    senal_dar_objetivo = pyqtSignal(str, str)
    senal_esconder_ventana_espera = pyqtSignal()
    senal_setear_baterias = pyqtSignal(object)

    def __init__(self, ruta_logo, ruta_nubes) -> None:
        super().__init__()
        self.ventana_inicio = VentanaInicio(ruta_logo, ruta_nubes)
        self.ventana_espera = VentanaEspera()
        self.ventana_juego = VentanaJuego()

        self.dict_jugadores_activos = dict()

        self.conexiones()

    def conexiones(self):
        # Ventana inicio
        self.ventana_inicio.senal_intentar_ingreso.connect(self.intentar_ingreso_sala_espera)
        self.senal_respuesta_ingreso_sala_espera.connect(self.ventana_inicio.tramitar_ingreso)

        # Ventana espera
        self.senal_abrir_ventana_espera.connect(self.ventana_espera.inicializar_usuario)
        self.ventana_espera.senal_iniciar_juego.connect(self.iniciar_juego)
        self.ventana_espera.senal_votar.connect(self.votar_mapa)
        self.senal_actualizar_votos.connect(self.ventana_espera.actualizar_votos)
        self.senal_nuevo_usuario.connect(self.ventana_espera.nuevo_usuario)
        self.senal_esconder_ventana_espera.connect(self.ventana_espera.esconderse)

        # Ventana juego

        self.senal_inicializar_jugadores_en_juego.connect(self.ventana_juego.definir_jugadores)
        self.senal_inscribir_jugador_en_juego.connect(self.ventana_juego.configurar_mi_nombre)
        self.senal_enviar_imagen_a_juego.connect(self.ventana_juego.recibir_imagen_de_perfil)
        self.senal_definir_mapa_en_juego.connect(self.ventana_juego.configurar_mapa)
        self.senal_dar_objetivo.connect(self.ventana_juego.definir_objetivo)
        self.senal_setear_baterias.connect(self.ventana_juego.setear_baterias)
        
    
    def manejar_mensaje(self, mensaje):
        '''
        Recibe un diccionario que le envía el cliente, y realiza la acción
        que este le indica
        '''
        accion = mensaje["comando"]
        # Ventana inicio
        if accion == "ingreso aceptado":
            self.aceptar_usuario_a_espera(mensaje["nombre"],\
                mensaje["color usuario"], mensaje["jefe"])
            
        elif accion == "ingreso denegado":
            causal = mensaje["causal"]
            if causal == "cupos":
                self.denegar_usuario_a_espera("cupos")
            elif causal == "nombre":
                self.denegar_usuario_a_espera("nombre")
            else:
                raise ValueError("La causal no se encuentra en mis registros")
        # Ventana espera
        elif accion == "actualizacion votos":
            self.actualizar_votos_en_sala_espera(mensaje)

        elif accion == "nuevo usuario":
            self.nuevo_usuario(mensaje)
        # Ventana juego
        elif accion == "inicializar jugadores en juego":
            self.inicializar_jugadores_en_juego(mensaje["jugadores e info"])
        elif accion == "mapa a usar en juego":
            self.definir_mapa_en_juego(mensaje["mapa"])
        elif accion == "dar objetivo":
            self.dar_objetivos_de_juego(mensaje["desde"], mensaje["hasta"])
        elif accion == "baterias iniciales":
            self.setear_baterias(mensaje["baterias"])
        else:
            raise ValueError("La acción no está en mis registros")
    
    def manejar_imagen(self, imagen_en_bytes, color):
        print(f"recibí imagen de color {color}, y el usuario es de color {self.int_color_usuario}")
        if color == self.int_color_usuario:
            self.imagen_propia = imagen_en_bytes
            print("Definí mi propia imagen")
        else:
            print("Enviaré una imagen al juego")
            self.senal_enviar_imagen_a_juego.emit(imagen_en_bytes, color)
    
    # ----------------------------- Ventana inicio

    def intentar_ingreso_sala_espera(self, nombre):
        diccionario = {
            "comando": "intentar ingreso sala de espera",
            "nombre": nombre
        }
        self.enviar_mensaje_a_servidor(diccionario)

    def enviar_mensaje_a_servidor(self, diccionario):
        self.senal_enviar_mensaje.emit(diccionario)
    
    def aceptar_usuario_a_espera(self, nombre, n_color, es_jefe):
        self.nombre_usuario = nombre
        self.int_color_usuario = n_color
        self.senal_respuesta_ingreso_sala_espera.emit(True, "True")
        self.senal_abrir_ventana_espera.emit(nombre, n_color, es_jefe)
        self.dict_jugadores_activos[n_color] = nombre
        self.senal_inscribir_jugador_en_juego.emit(nombre)
    
    def denegar_usuario_a_espera(self, motivo):
        self.senal_respuesta_ingreso_sala_espera.emit(False, motivo)

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
    
    def nuevo_usuario(self, mensaje):
        self.senal_nuevo_usuario.emit(mensaje["nombre"], mensaje["color usuario"])
    
    def actualizar_votos_en_sala_espera(self, dict_):
        self.senal_actualizar_votos.emit(dict_["nombres votadores"],
            dict_["san joaquin"], dict_["ingenieria"])
    
    # ------------------------------- Ventana juego

    def inicializar_jugadores_en_juego(self, lista):
        self.senal_inicializar_jugadores_en_juego.emit(lista)
        self.senal_enviar_imagen_a_juego.emit(self.imagen_propia, self.int_color_usuario)
        self.senal_esconder_ventana_espera.emit()
    
    def definir_mapa_en_juego(self, mapa):
        self.senal_definir_mapa_en_juego.emit(mapa)
    
    def dar_objetivos_de_juego(self, desde, hasta):
        self.senal_dar_objetivo.emit(desde, hasta)
    
    def setear_baterias(self, baterias):
        self.senal_setear_baterias.emit(baterias)