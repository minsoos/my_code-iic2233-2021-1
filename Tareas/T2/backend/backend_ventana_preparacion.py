import parametros as p
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
import parametros as p
from backend.personajes import Homero, Lisa, Moe, Krusty, Personaje
from random import randint
from time import time


class LogicaVentanaPreparacion(QObject):

    senal_actualizar_info_ventana = pyqtSignal(int, int, int, int, int)
    # Se envía número de ronda, puntaje acumulado, ítems buenos, malos y vida; en ese orden
    senal_actualizar_animacion_personaje = pyqtSignal(str)
    senal_actualizar_movimiento_personaje = pyqtSignal(tuple)
    senal_ocultar_ventana = pyqtSignal(bool)
    senal_abrir_ventana_juego = pyqtSignal(str, Personaje, int, str)
    # Se envía edificio, personaje, número de ronda y dificultad; en ese orden
    senal_abrir_ventana_error = pyqtSignal()
    senal_mostrar_ventana = pyqtSignal()

    def __init__(self) -> None:
        '''
        Backend de VentanaPreparacion. Aquí se cargan los
        valores de los parámetros correspondientes, además,
        maneja la entrada y salida de esta ventana
        '''
        super().__init__()
        self.dificultad = "intro"

    def iniciar_nueva_partida(self, nombre):
        self.nombre_de_usuario = nombre
        self.numero_de_ronda = 1
        self.puntaje_acumulado = 0
        self.items_buenos = 0
        self.items_malos = 0
        self.personaje_actual = None
        self.posicion_personaje = None
        self.personajes = {
            "homero": Homero(),
            "lisa": Lisa(),
            "moe": Moe(),
            "krusty": Krusty()
        }
        self.senal_actualizar_info_ventana.emit(1, 0, 0, 0, 0)
        self.conexiones()
    
    def conexiones(self):
        for personaje in self.personajes:
            persona = self.personajes[personaje]
            persona.senal_mover_personaje.connect(self.movimiento_de_personaje)
            persona.senal_actualizar_animacion.connect(self.animacion_de_personaje)

    # --------------------------- Aquí termina la inicialización
    # --------------------------- Aquí empieza la actualización de info y parámetros

    def actualizar_info_ventana(self):
        a = self.numero_de_ronda
        b = self.puntaje_acumulado
        c = self.items_buenos
        d = self.items_malos
        if self.personaje_actual is not None:
            e = self.personaje_actual.vida*100
        else:
            e = 0
        self.senal_actualizar_info_ventana.emit(a, b, c, d, e)

    def cambiar_personaje(self, personaje, posicion):
        personaje = self.personajes[personaje]
        if not self.personaje_actual is None:
            # Acá paramos el QTimer del personaje anterior
            self.personaje_actual.timer.stop()
        self.personaje_actual = personaje
        self.posicion_personaje = posicion
        self.inicializar_mapa_en_personaje(posicion)
        self.actualizar_info_ventana()
        self.movimiento_de_personaje_solicitado("w")
        self.personaje_actual.timer.start()
    
    def inicializar_mapa_en_personaje(self, posicion):
        '''
        Le da los argumentos del mapa a personaje
        '''
        a = p.RECTANGULO_TABLERO_PREPARACION
        b = posicion
        c = self.dificultad
        self.personaje_actual.inicializador_de_mapa("preparacion", a, b, c)

    # ------------------------------------ Desde acá se actualiza al label (moverse/animación)

    def movimiento_de_personaje_solicitado(self, tecla):
        # --------------------acoplado
        if self.personaje_actual is not None:
            self.personaje_actual.recibidor_de_mover(tecla)

    def animacion_de_personaje(self, path_dado):
        self.senal_actualizar_animacion_personaje.emit(path_dado)

    def movimiento_de_personaje(self, posicion_nueva):
        self.posicion_personaje = posicion_nueva
        self.senal_actualizar_movimiento_personaje.emit(posicion_nueva)

    # ----------------------------------- Desde acá se revisa la entrada a edificios

    def revision_solicitud_entrada_a_edificio(self, edificio, dificultad):
        if edificio == "primaria" and self.personaje_actual.nombre == "lisa" or\
            edificio == "planta" and self.personaje_actual.nombre == "homero" or\
            edificio == "bar" and self.personaje_actual.nombre == "moe" or\
            edificio == "krustyland" and self.personaje_actual.nombre == "krusty":
            puede = True
        else:
            puede = False
        if puede:
            self.entrar_a_juego(edificio, dificultad)
        else:
            self.senal_abrir_ventana_error.emit()

    def entrar_a_juego(self, edificio, dificultad):
        self.senal_ocultar_ventana.emit(True)
        for personaje in self.personajes:
            persona = self.personajes[personaje]
            persona.senal_mover_personaje.disconnect()
            persona.senal_actualizar_animacion.disconnect()
        a = edificio
        b = self.personaje_actual
        c = self.numero_de_ronda
        d = dificultad
        self.senal_abrir_ventana_juego.emit(a, b, c, d)
    
    # ----------------------------------- Otros

    def cheats(self, combinacion):
        '''
        Comprueba si se ejecutó el cheat de aumentar vida
        y lo ejecuta
        '''
        if "v" in combinacion and "i" in combinacion and "d" in combinacion:
            self.personaje_actual.vida += p.VIDA_TRAMPA
            self.actualizar_info_ventana()

    def boton_salir_presionado(self):
        self.guardar_puntuacion(0, 0, 0)

    def guardar_puntuacion(self, puntaje, i_buenos, i_malos):
        self.numero_de_ronda += 1
        self.puntaje_acumulado += puntaje
        self.items_buenos += i_buenos
        self.items_malos += i_malos
        self.senal_ocultar_ventana.emit(True)
        self.escribir_ranking()
    
    def escribir_ranking(self):
        if self.puntaje_acumulado > 0:
            with open(p.RUTA_RANKING, "a", encoding="UTF-8") as archivo:
                archivo.write(f"{self.nombre_de_usuario},{self.puntaje_acumulado}\n")

    # ---------------------------------- Volver a ventana
    
    def volver_a_ventana(self, puntaje, i_buenos, i_malos):
        self.numero_de_ronda += 1
        self.puntaje_acumulado += puntaje
        self.items_buenos += i_buenos
        self.items_malos += i_malos
        self.inicializar_mapa_en_personaje(p.POSICION_DESAPARECER_PERSONAJE)
        self.personaje_actual = None
        #
        self.actualizar_info_ventana()
        # Esto es para "iniciar al personaje" artificialmente, se mueve un espacio hacia arriba
        self.senal_mostrar_ventana.emit()
        self.conexiones()
    
    