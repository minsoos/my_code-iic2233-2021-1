from codificacion import codificar_imagen
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from random import choice
from utils import cargar_parametros, normalizar_ruta
from collections import namedtuple



class Logica(QObject):

    senal_enviar_mensaje = pyqtSignal(int, object)
    senal_enviar_imagen = pyqtSignal(int, str)
    senal_eliminar_cliente = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.usuarios_activos = {}
        self.conteo_votaciones = {
            "ingenieria": 0,
            "san joaquin": 0
        }

        self.parametros = cargar_parametros("parametros.json")
        for parametro in self.parametros["RUTAS"]["IMAGENES_PERFIL"]:
            ruta = normalizar_ruta(self.parametros["RUTAS"]["IMAGENES_PERFIL"][parametro])
            self.parametros["RUTAS"]["IMAGENES_PERFIL"][parametro] = ruta
    
    def enviar_mensaje_a_usuario(self, id_usuario, diccionario):
        print(f"enviaré el mensaje {diccionario}")
        self.senal_enviar_mensaje.emit(id_usuario, diccionario)
    
    def enviar_imagen_a_usuario(self, id_usuario, path_imagen):
        self.senal_enviar_imagen.emit(id_usuario, path_imagen)

    def caracterizar_mensaje(self, id_usuario, dict_):
        comando = dict_["comando"]
        print("caracterizando mensaje")
        if comando == "intentar ingreso sala de espera":
            print("comprobaré nombre de usuario")
            self.comprobar_nombre_de_usuario(id_usuario, dict_["nombre"])
        elif comando == "iniciar juego":
            self.iniciar_juego()
        elif comando == "votar":
            self.votacion_de_mapa(id_usuario, dict_["voto"])
        else:
            print("nosé qué me pediste (soy servidor/logica)")
        
    def comprobar_nombre_de_usuario(self, id_usuario, nombre):
        parametro_n_usuarios = self.parametros["CANTIDAD_JUGADORES_PARTIDA"]
        if nombre not in self.usuarios_activos and\
            len(self.usuarios_activos) < parametro_n_usuarios and len(nombre) <= 15:
            self.inicializar_usuario(id_usuario, nombre)
        elif len(self.usuarios_activos) >= parametro_n_usuarios:
            diccionario = {
                "comando": "ingreso denegado",
                "causal": "cupos"}
            self.enviar_mensaje_a_usuario(id_usuario, diccionario)
        else:
            diccionario = {
                "comando": "ingreso denegado",
                "causal": "nombre"}
            self.enviar_mensaje_a_usuario(id_usuario, diccionario)

    def inicializar_usuario(self, id_usuario, nombre):
        colores_disponibles = {1, 2, 3, 4} - set(map(lambda x: x["color"],
            self.usuarios_activos.values()))
        color_usuario = choice(list(colores_disponibles))
        print("le dimos el color", color_usuario)
        self.usuarios_activos[id_usuario] = {
            "color": color_usuario,
            "nombre": nombre
        }
        jefatura = len(self.usuarios_activos) == 1

        diccionario = {
            "comando": "ingreso aceptado",
            "color usuario": color_usuario,
            "nombre": nombre,
            "jefe": jefatura
        }
        self.enviar_mensaje_a_usuario(id_usuario, diccionario)
        self.enviar_imagen_a_nuevo_usuario(id_usuario, color_usuario)

        for usuario_n in self.usuarios_activos:
            if usuario_n != id_usuario:
                usuario_n = self.usuarios_activos[usuario_n]
                diccionario = {
                    "comando": "nuevo usuario",
                    "color usuario": usuario_n["color"],
                    "nombre": nombre
                }
                self.enviar_mensaje_a_usuario(usuario_n, diccionario)

        diccionario = {
            "comando": "nuevo usuario",
            "color usuario": color_usuario,
            "nombre": nombre
        }

        for usuario_n in self.usuarios_activos:
            if usuario_n != id_usuario:
                self.enviar_mensaje_a_usuario(usuario_n, diccionario)
    
    def enviar_imagen_a_nuevo_usuario(self, id_usuario, color):
        path_color = self.parametros["RUTAS"]["IMAGENES_PERFIL"][str(color)]
        self.enviar_imagen_a_usuario(id_usuario, path_color)

    
    def desconectar_usuario(self, id_usuario):
        self.usuarios_activos.pop(id_usuario)
    
    # ---------------------------------- Sala de espera

    def votacion_de_mapa(self, id_usuario, voto):
        if voto == "ingenieria":
            self.conteo_votaciones["ingenieria"] += 1
        elif voto == "san joaquin":
            self.conteo_votaciones["san joaquin"] += 1
        else:
            raise ValueError("El voto fue inválido")

        diccionario = {
            "comando": "actualizacion votos",
            "san joaquin": self.conteo_votaciones["san joaquin"],
            "ingenieria": self.conteo_votaciones["ingenieria"],
            "nombre votador": self.usuarios_activos[id_usuario]["nombre"]
        }
        
        for usuario in self.usuarios_activos:
            self.enviar_mensaje_a_usuario(usuario, diccionario)
    
    # ------------------------------ ventana juego
    
    def iniciar_juego(self):
        turnos_partida = [i for i in range(self.parametros["CANTIDAD_JUGADORES_PARTIDA"])]
        Jugador = namedtuple("Inicializador_jugadores_en_juego", ["nombre", "color", "turno"])
        lista_jugadores = list()
        for jugador in self.usuarios_activos:
            nombre = self.usuarios_activos[jugador]["nombre"]
            color = self.usuarios_activos[jugador]["color"]
            turno_n = choice(turnos_partida)
            turnos_partida.pop(turno_n)
            lista_jugadores.append(Jugador(nombre, color, turno_n))
        diccionario = {
            "comando": "inicializar jugadores en juego",
            "jugadores e info": lista_jugadores
        }
        for jugador in self.usuarios_activos:
            self.enviar_mensaje_a_usuario(jugador, diccionario)
        
        self.enviar_imagenes_de_perfil(lista_jugadores)
    
    def enviar_imagenes_de_perfil(self, lista):
        for jugador in lista:
            path_color = self.parametros["RUTAS"]["IMAGENES_PERFIL"][jugador.color]
            for usuario_a_enviar in self.usuarios_activos:
                if self.usuarios_activos[usuario_a_enviar]["color"] != jugador.color:
                    self.enviar_mensaje_a_usuario(usuario_a_enviar, path_color)


