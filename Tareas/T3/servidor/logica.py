from codificacion import codificar_imagen
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from random import choice, randint
from utils import cargar_parametros, normalizar_ruta, crear_mapa


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
        elif comando == "jugar turno":
            self.jugar_turno(id_usuario, dict_)
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
        turnos_partida = [i + 1 for i in range(self.parametros["CANTIDAD_JUGADORES_PARTIDA"])]
        self.turnos_de_jugadores = {}
        self.jugadores_segun_turno = {}
        lista_jugadores = list()
        for jugador in self.usuarios_activos:
            turno_n = randint(0, len(turnos_partida) - 1)
            turno_n = turnos_partida.pop(turno_n)
            dict_jugadores = {
                "nombre": self.usuarios_activos[jugador]["nombre"],
                "color": self.usuarios_activos[jugador]["color"],
                "turno": turno_n

            }
            self.turnos_de_jugadores[dict_jugadores["nombre"]] = turno_n
            self.jugadores_segun_turno[turno_n] = dict_jugadores["nombre"]
            lista_jugadores.append(dict_jugadores)
        self.turno_actual = 1
        diccionario = {
            "comando": "inicializar jugadores en juego",
            "jugadores e info": lista_jugadores
        }
        for jugador in self.usuarios_activos:
            self.enviar_mensaje_a_usuario(jugador, diccionario)

        self.enviar_imagenes_de_perfil(lista_jugadores)
        self.indicar_mapa_a_usar()
        self.crear_nodo_mapa()
        self.dar_objetivos_a_usuarios()
        self.dar_baterias()

    def enviar_imagenes_de_perfil(self, lista):
        for jugador in lista:
            color = str(jugador["color"])
            for usuario_a_enviar in self.usuarios_activos:
                if self.usuarios_activos[usuario_a_enviar]["color"] != jugador["color"]:
                    self.enviar_imagen_a_usuario(usuario_a_enviar, color)

    def indicar_mapa_a_usar(self):
        votos_sj = self.conteo_votaciones["san joaquin"]
        votos_ing = self.conteo_votaciones["ingenieria"]
        diccionario = {
            "comando": "mapa a usar en juego",
        }
        if votos_sj == votos_ing:
            elegido = randint(1, 2)
            if elegido == 1:
                self.mapa_de_juego = "san joaquin"
                diccionario["mapa"] = "san joaquin"
            elif elegido == 2:
                self.mapa_de_juego = "ingenieria"
                diccionario["mapa"] = "ingenieria"
        elif votos_ing > votos_sj:
            self.mapa_de_juego = "ingenieria"
            diccionario["mapa"] = "ingenieria"
        elif votos_ing < votos_sj:
            self.mapa_de_juego = "san joaquin"
            diccionario["mapa"] = "san joaquin"

        for usuario in self.usuarios_activos:
            self.enviar_mensaje_a_usuario(usuario, diccionario)

    def crear_nodo_mapa(self):
        mapa = self.mapa_de_juego
        self.diccionario_nodos = crear_mapa("mapa.json", mapa)

    def dar_objetivos_a_usuarios(self):
        self.objetivos = {}
        for usuario in self.usuarios_activos:
            completado = False
            while not completado:
                nodo_a = choice(list(self.diccionario_nodos.keys()))
                nodo_b = choice(list(self.diccionario_nodos.keys()))
                if nodo_a != nodo_b:
                    completado = self.diccionario_nodos[nodo_a].es_su_vecino(nodo_b)
                    completado = not completado
            
            self.objetivos[self.usuarios_activos[usuario]["nombre"]] = {
                "desde": nodo_a,
                "hasta": nodo_b
            }
            
            diccionario = {
                "comando": "dar objetivo",
                "desde": nodo_a,
                "hasta": nodo_b
            }
            print("enviaré el objetivo al usuario")
            self.senal_enviar_mensaje.emit(usuario, diccionario)
    
    def dar_baterias(self):
        self.baterias = {}
        for usuario in self.usuarios_activos:
            baterias_minimas = self.parametros["BATERIAS_MIN"]
            baterias_maximas = self.parametros["BATERIAS_MAX"]
            baterias_usuario = randint(baterias_minimas, baterias_maximas)
            self.baterias[self.usuarios_activos[usuario]["nombre"]] = baterias_usuario
        
        self.enviar_info_baterias()
    
    def enviar_info_baterias(self):
        diccionario = {
                "comando": "setear baterias",
                "baterias": self.baterias,
            }
        for usuario in self.usuarios_activos:
            self.enviar_mensaje_a_usuario(usuario, diccionario)
    
    def jugar_turno(self, id_usuario, diccionario):
        nombre_jugador = self.usuarios_activos[id_usuario]
        if self.turnos_de_jugadores[nombre_jugador] == self.turno_actual:
            accion = diccionario["accion"]
            if accion == "comprar camino":
                self.intentar_comprar_camino(id_usuario, diccionario["desde"], diccionario["hasta"])
            elif accion == "sacar carta":
                self.sacar_carta(id_usuario)

            if (self.turno_actual + 1) in self.turnos_de_jugadores.values():
                self.turno_actual += 1
            else:
                self.turno_actual = 1
            

            diccionario = {
                "comando": "cambiar turno",
                "turno actual": self.jugadores_segun_turno[self.turno_actual]
            }
            for jugador in self.usuarios_activos:
                self.enviar_mensaje_a_usuario(jugador, diccionario)
    
    def intentar_comprar_camino(self, id_usuario, desde, hasta):
        diccionario_preventivo = {
            "comando": "anunciar error"
        }

        nombre_jugador = self.usuarios_activos[id_usuario]
        desde, hasta = desde.upper(), hasta.upper()
        nombre_nodos = self.diccionario_nodos.keys()
        primera_condicion = desde in nombre_nodos
        segunda_condicion = hasta in nombre_nodos
        if primera_condicion and segunda_condicion:
            nodo_inicial = self.diccionario_nodos[desde]
            if nodo_inicial.es_su_vecino(hasta):
                camino = nodo_inicial.encontrar_camino_con(hasta)
                if camino is None:
                    raise ValueError("El camino no está en los posibles")
 
                presio = camino.costo
                if self.baterias[nombre_jugador] - presio >= 0:
                    self.baterias[nombre_jugador] -= presio
                    print("Aquí debo modificar los puntajes")
                    self.enviar_info_baterias()
                    self.enviar_pintada_de_camino(id_usuario, camino)
                else:
                    diccionario_preventivo["mensaje"] = "No tienes suficiente dinero"
                    self.enviar_mensaje_a_usuario(id_usuario, diccionario_preventivo)
            else:
                diccionario_preventivo["mensaje"] = "El camino que quieres comprar no existe"
                self.enviar_mensaje_a_usuario(id_usuario, diccionario_preventivo)
        else:
            diccionario_preventivo["mensaje"] = "Los nodos que indicas no son válidos"
            self.enviar_mensaje_a_usuario(id_usuario, diccionario_preventivo)
    
    def enviar_pintada_de_camino(self, id_usuario, camino):
        pos_nodo_1 = camino.nodo_1.x, camino.nodo_1.y
        pos_nodo_2 = camino.nodo_2.x, camino.nodo_2.y
        color = self.usuarios_activos[id_usuario]["color"]
        diccionario = {
            "comando": "pintar camino",
            "color": color,
            "desde": pos_nodo_1,
            "hasta": pos_nodo_2
        }
        for jugador in self.usuarios_activos:
            self.enviar_mensaje_a_usuario(jugador, diccionario)

