from codificacion import codificar_imagen
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from random import choice, randint
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
        self.usuarios_que_votaron = []

        self.parametros = cargar_parametros("parametros.json")
        for parametro in self.parametros["RUTAS"]["IMAGENES_PERFIL"]:
            ruta = normalizar_ruta(self.parametros["RUTAS"]["IMAGENES_PERFIL"][parametro])
            self.parametros["RUTAS"]["IMAGENES_PERFIL"][parametro] = ruta
    
    def enviar_mensaje_a_usuario(self, id_usuario, diccionario):
        '''
        Recibe el id de un usuario y un diccionario a enviar y se encarga de
        mandarle al servidor que lo mande
        '''
        print(f"enviaré el mensaje {diccionario}")
        self.senal_enviar_mensaje.emit(id_usuario, diccionario)

    def caracterizar_mensaje(self, id_usuario, dict_):
        comando = dict_["comando"]
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
    
    def enviar_imagen_a_usuario(self, id_usuario, color):
        path_color = self.parametros["RUTAS"]["IMAGENES_PERFIL"][str(color)]
        print("emitiré la señal para enviar una imagen")
        self.senal_enviar_imagen.emit(id_usuario, path_color)

    def desconectar_usuario(self, id_usuario):
        self.usuarios_activos.pop(id_usuario)

    # ---------------------------------- Sala de espera

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

        # Enviar el usuario inicializado al resto de los usuarios

        diccionario = {
            "comando": "nuevo usuario",
            "color usuario": color_usuario,
            "nombre": nombre
        }
        for usuario_n in self.usuarios_activos:
            if usuario_n != id_usuario:
                self.enviar_mensaje_a_usuario(usuario_n, diccionario)
        
        # Enviar el resto de los usuarios al usuario ingresado

        for usuario_n in self.usuarios_activos:
            if usuario_n != id_usuario:
                #print(f"Enviaré al usuario {self.usuarios_activos[usuario_n]["nombre"]}")
                usuario_i = self.usuarios_activos[usuario_n]
                diccionario = {
                    "comando": "nuevo usuario",
                    "color usuario": usuario_i["color"],
                    "nombre": usuario_i["nombre"]
                }
                self.enviar_mensaje_a_usuario(id_usuario, diccionario)
        
        # Actualización de sistema de votos

        diccionario = {
            "comando": "actualizacion votos",
            "san joaquin": self.conteo_votaciones["san joaquin"],
            "ingenieria": self.conteo_votaciones["ingenieria"],
            "nombres votadores": self.usuarios_que_votaron
        }
        self.enviar_mensaje_a_usuario(id_usuario, diccionario)

        self.enviar_imagen_a_usuario(id_usuario, color_usuario)

    def votacion_de_mapa(self, id_usuario, voto):
        if voto == "ingenieria":
            self.conteo_votaciones["ingenieria"] += 1
        elif voto == "san joaquin":
            self.conteo_votaciones["san joaquin"] += 1
        else:
            raise ValueError("El voto fue inválido")
        
        self.usuarios_que_votaron.append(self.usuarios_activos[id_usuario]["nombre"])

        diccionario = {
            "comando": "actualizacion votos",
            "san joaquin": self.conteo_votaciones["san joaquin"],
            "ingenieria": self.conteo_votaciones["ingenieria"],
            "nombres votadores": self.usuarios_que_votaron
        }


        
        for usuario in self.usuarios_activos:
            self.enviar_mensaje_a_usuario(usuario, diccionario)
    
    # ------------------------------ ventana juego
    
    def iniciar_juego(self):
        turnos_partida = [i for i in range(self.parametros["CANTIDAD_JUGADORES_PARTIDA"])]
        Jugador = namedtuple("Inicializador_jugadores_en_juego", ["nombre", "color", "turno"])
        lista_jugadores = list()
        for jugador in self.usuarios_activos:
            turno_n = randint(0, len(turnos_partida) - 1)
            turno_n = turnos_partida.pop(turno_n) +1
            dict_jugadores = {
                "nombre": self.usuarios_activos[jugador]["nombre"],
                "color": self.usuarios_activos[jugador]["color"],
                "turno": turno_n

            }
            lista_jugadores.append(dict_jugadores)
        diccionario = {
            "comando": "inicializar jugadores en juego",
            "jugadores e info": lista_jugadores
        }
        for jugador in self.usuarios_activos:
            self.enviar_mensaje_a_usuario(jugador, diccionario)
        
        self.enviar_imagenes_de_perfil(lista_jugadores)
    
    def enviar_imagenes_de_perfil(self, lista):
        for jugador in lista:
            color = str(jugador["color"])
            for usuario_a_enviar in self.usuarios_activos:
                if self.usuarios_activos[usuario_a_enviar]["color"] != jugador["color"]:
                    self.enviar_imagen_a_usuario(usuario_a_enviar, color)


