from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from random import choice


class Logica(QObject):

    senal_enviar_mensaje = pyqtSignal(int, object)

    def __init__(self) -> None:
        super().__init__()
        self.usuarios_activos = {}

    def enviar_mensaje_a_servidor(self, id_usuario, diccionario):
        self.senal_enviar_mensaje.emit(id_usuario, diccionario)

    def caracterizar_mensaje(self, id_usuario, dict_):
        comando = dict_["comando"]
        print("caracterizando mensaje")
        if comando == "intentar ingreso sala de espera":
            print("comprobaré nombre de usuario")
            self.comprobar_nombre_de_usuario(id_usuario, dict_["nombre"])
        elif comando == "iniciar juego":
            self.iniciar_juego()
        elif comando == "votar":
            self.votacion_de_mapa(dict_["voto"])
        else:
            print("nosé qué me pediste")
        
    def comprobar_nombre_de_usuario(self, id_usuario, nombre):
        if nombre not in self.usuarios_activos and\
            len(self.usuarios_activos) < 4 and len(nombre) <= 15:
            self.inicializar_usuario(id_usuario, nombre)
        elif len(self.usuarios_activos) >= 4:
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
        colores_disponibles = {1, 2, 3, 4} - set(self.usuarios_activos.values())
        color_usuario = choice(list(colores_disponibles))
        print("le dimos el color", color_usuario)
        self.usuarios_activos[id_usuario] = color_usuario

        diccionario = {
            "comando": "ingreso aceptado",
            "color usuario": color_usuario,
            "nombre": nombre,
            
        }
        self.enviar_mensaje_a_usuario(id_usuario, diccionario)
    
    def desconectar_usuario(self, id_usuario):
        self.usuarios_activos.pop(id_usuario)
    
    def enviar_mensaje_a_usuario(self, id_usuario, diccionario):
        print(f"enviaré el mensaje {diccionario}")
        self.senal_enviar_mensaje.emit(id_usuario, diccionario)
    
    # ---------------------------------- Sala de espera

    def iniciar_juego(self):
        pass

    def votacion_de_mapa(self):
        pass

            
