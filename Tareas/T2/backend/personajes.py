from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
import parametros as p
from time import sleep
from collections import deque
from os import path


class Personaje(QObject):

    senal_mover_personaje = pyqtSignal(tuple)
    senal_actualizar_animacion = pyqtSignal(str)
    senal_no_vida = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.__vida = 1
        self.moviendo = "up"
        self.transicion_animacion = "3"
        self.label_personaje = None
        self.label_personaje_posible = None # Se utiliza para hacer pruebas con él
        self.labels_obstaculos = None
        self.rectangulo_juego = None
        self.velocidad = None
        self.posicion = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.animacion)
        self.timer.setInterval(1000*0.1)
        self.rutas_personajes = p.RUTAS_PERSONAJES

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, nuevo_valor):
        if nuevo_valor <= 0:
            self.__vida = 0
            self.aviso_no_vida()
        elif nuevo_valor > 1:
            self.__vida = 1
            print("no cabía más vida")
        elif nuevo_valor <= 1:
            self.__vida = nuevo_valor
        else:
            raise ValueError("La vida no se seteó bien")

    def inicializador_de_mapa(self, tipo_tablero, rectangulo_juego, posicion_inicial, dificultad):
        self.tipo_tablero = tipo_tablero
        self.rectangulo_juego =rectangulo_juego
        self.posicion = posicion_inicial
        self.dificultad = dificultad

    def recibidor_de_mover(self, tecla):
        '''
        recibe una tecla apretada, si está entre wasd modifica
        self.moviendo, sino, no hace nada
        '''
        # Da el movimiento de acuerdo a la letra presionada
        if tecla == "w":
            movimiento = "up"
        elif tecla == "s":
            movimiento = "down"
        elif tecla == "a":
            movimiento = "left"
        elif tecla == "d":
            movimiento = "right"
        else:
            raise ValueError("En personaje")

        # Cambia la orientación del personaje si es distinta a la actual
        if movimiento != self.moviendo:
            self.moviendo = movimiento
            if movimiento == "up":
                imagen = "up_3.png"
            elif movimiento == "down":
                imagen = "down_3.png"
            elif movimiento == "left":
                imagen = "left_2.png"
            elif movimiento == "right":
                imagen = "right_2.png"
            else:
                raise ValueError("algo raro, recibidor de mover")
            rutas_movimiento = path.join(self.rutas_personajes[self.nombre], imagen)
            self.senal_actualizar_animacion.emit(rutas_movimiento)

        self.moverse()

    def moverse(self):
        '''
        cambia el atributo posicion, llama
         y emite cambiar_posicion
        '''
        if not self.timer.isActive():
            self.timer.start()
        if self.moviendo == "up":
            nueva_pos = (self.posicion[0], self.posicion[1] - self.velocidad)
        elif self.moviendo == "down":
            nueva_pos = (self.posicion[0], self.posicion[1] + self.velocidad)
        elif self.moviendo == "left":
            nueva_pos = (self.posicion[0] - self.velocidad, self.posicion[1])
        elif self.moviendo == "right":
            nueva_pos = (self.posicion[0] + self.velocidad, self.posicion[1])

        r = self.rectangulo_juego
        if r[0] < nueva_pos[0] < r[0] + r[2] and r[1] < nueva_pos[1] < r[1] + r[3]:
            if self.puede_pasar_en_juego(nueva_pos):
                self.posicion = nueva_pos
                self.senal_mover_personaje.emit(self.posicion)

    def puede_pasar_en_juego(self, nueva_pos):
        '''
        Esta función revisa si se está en un juego (lo que implicaría
        revisar obstáculos, y permite o no el movimiento)
        si no está en juego, retorna True
        '''
        if self.tipo_tablero == "juego":
            self.label_personaje_posible = self.label_personaje
            self.label_personaje_posible.move(*nueva_pos)
            obstaculizado = False
            rect_personaje = self.label_personaje_posible.geometry()
            for obstaculo in self.labels_obstaculos:
                rect_obstaculo = obstaculo.geometry()
                if rect_personaje.intersects(rect_obstaculo):
                    obstaculizado = True
            if not obstaculizado:
                return True
            else:
                return False
        return True

    def animacion(self):
        if self.transicion_animacion == "3":
            self.transicion_animacion = "2"
        elif self.transicion_animacion == "2":
            self.transicion_animacion = "1"
        elif self.transicion_animacion == "1":
            self.transicion_animacion = "3"
        else:
            raise ValueError("raro en animación")
        archivo = f"{self.moviendo}_{self.transicion_animacion}.png"
        nuevo_label = path.join(self.rutas_personajes[self.nombre], archivo)
        self.senal_actualizar_animacion.emit(nuevo_label)
        self.timer.stop()



    def aviso_no_vida(self):
        '''
        Avisa con una señal que al personaje no le queda vida
        '''
        self.senal_no_vida.emit()

        

class Homero(Personaje):
    def __init__(self) -> None:
        self.nombre = "homero"
        super().__init__()
        self.velocidad = p.VELOCIDAD_HOMERO

class Lisa(Personaje):
    def __init__(self) -> None:
        self.nombre = "lisa"
        super().__init__()
        self.velocidad = p.VELOCIDAD_LISA

class Krusty(Personaje):
    def __init__(self) -> None:
        self.nombre = "krusty"
        super().__init__()
        self.velocidad = p.VELOCIDAD_KRUSTY

class Moe(Personaje):
    def __init__(self) -> None:
        self.nombre = "moe"
        super().__init__()
        self.velocidad = p.VELOCIDAD_MOE

# -------------------------------- Desde aquí empieza gorgory


class CronometroSegundos(QObject):

    def __init__(self) -> None:
        super().__init__()
        self.segundos = 0
        self.pausado = False
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.pasar_tiempo)
        self.timer.start()

    def pasar_tiempo(self):
        self.segundos += 0.01

    def pausar(self):
        if self.pausado:
            self.timer.start()
            print("cronometro reanudado")
            self.pausado = False
        else:
            self.timer.stop()
            print("cronometro pausado")
            self.pausado = True


class Gorgory(QThread):

    senal_mover_gorgory = pyqtSignal(tuple)
    senal_animacion_gorgory = pyqtSignal(str)
    senal_pedir_actualizacion = pyqtSignal()

    def __init__(self, dificultad, nombre_adversario) -> None:
        self.nombre = "gorgory"
        super().__init__()
        self.moviendo = "up"
        self.transicion_animacion = "3"
        self.posicion = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.animacion)
        self.timer.setInterval(1000*0.1)
        self.timer.start()
        self.empezo = False
        self.rutas_personajes = p.RUTAS_PERSONAJES
        self.tiempo_de_pausa = 0
        if dificultad == "intro":
            tiempo_delay = p.TIEMPO_DELAY_INTRO
        elif dificultad == "avanzada":
            tiempo_delay = p.TIEMPO_DELAY_AVANZADA
        if nombre_adversario == "krusty":
            tiempo_delay *= 2
        self.delay = tiempo_delay
        #
        self.posiciones_historicas = deque()
        self.pausa = False
        self.cronometro = CronometroSegundos()
        self.horario_actual = self.cronometro.segundos
    
    def recibir_posicion(self, posicion):
        horario_antiguo = self.horario_actual
        self.horario_actual = self.cronometro.segundos
        tiempo_intermedio = self.horario_actual - horario_antiguo
        self.posiciones_historicas.append((tiempo_intermedio, posicion))
    
    def dar_posicion_inicial(self, posicion):
        self.posicion = posicion

    def pausar(self):
        if self.pausa:
            self.pausa = False
            self.timer.start()
            self.cronometro.pausar()
        elif not self.pausa:
            self.pausa = True
            self.timer.stop()
            self.cronometro.pausar()

    def run(self):
        while self.cronometro.segundos < self.delay:
            sleep(0.1)
        self.empezo = True
        while len(self.posiciones_historicas) > 0:
            if not self.pausa:
                argumento = self.posiciones_historicas.popleft()
                tiempo_intermedio = argumento[0]
                posicion = argumento[1]
                sleep(tiempo_intermedio)
                if posicion[1] - self.posicion[1] < 0:
                    movimiento = "up"
                elif posicion[1] - self.posicion[1] > 0:
                    movimiento = "down"
                elif posicion[0] - self.posicion[0] < 0:
                    movimiento = "left"
                elif posicion[0] - self.posicion[0] > 0:
                    movimiento = "right"
                if movimiento != self.moviendo:
                    self.moviendo = movimiento
                    if movimiento == "up":
                        imagen = "up_3.png"
                    elif movimiento == "down":
                        imagen = "down_3.png"
                    elif movimiento == "left":
                        imagen = "left_2.png"
                    elif movimiento == "right":
                        imagen = "right_2.png"
                    else:
                        raise ValueError("algo raro, recibidor de mover")
                    rutas_movimiento = path.join(self.rutas_personajes[self.nombre], imagen)
                    self.senal_animacion_gorgory.emit(rutas_movimiento)
                self.posicion = posicion
                self.senal_mover_gorgory.emit(posicion)

    def animacion(self):
        if self.transicion_animacion == "3":
            self.transicion_animacion = "2"
        elif self.transicion_animacion == "2":
            self.transicion_animacion = "1"
        elif self.transicion_animacion == "1":
            self.transicion_animacion = "3"
        else:
            raise ValueError("raro en animación")
        archivo = f"{self.moviendo}_{self.transicion_animacion}.png"
        nuevo_label = path.join(self.rutas_personajes[self.nombre], archivo)
        if self.empezo:
            self.senal_animacion_gorgory.emit(nuevo_label)

