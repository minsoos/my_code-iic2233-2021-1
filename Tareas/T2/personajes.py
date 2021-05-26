from abc import ABC
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QEventLoop, Qt
import parametros as p
from os import path

class Personaje(QObject):

    senal_mover_personaje = pyqtSignal(tuple)
    senal_actualizar_animacion= pyqtSignal(str)

    def __init__(self, rectangulo_juego=(10,290,850,460)) -> None:
        super().__init__()
        self.__vida = 1
        self.moviendo = "up"
        self.transicion_animacion = "3"
        self.label_personaje = None
        self.label_personaje_posible = None
        self.labels_obstaculos = None
        self.rectangulo_juego = rectangulo_juego
        self.velocidad = None
        self.posicion = None
        self.limites_posicion = None
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

        elif nuevo_valor <= 1:
            self.__vida = nuevo_valor
        else:
            raise ValueError("La vida no se seteó bien")


    def recibidor_de_mover(self, tecla):
        '''
        recibe una tecla apretada, si está entre wasd modifica
        self.moviendo, sino, no hace nada
        '''
        print("recibidor de mover")
        if tecla == "w":
            movimiento = "up"
        elif tecla == "s":
            movimiento = "down"
        elif tecla == "a":
            movimiento = "left"
        elif tecla == "d":
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
            self.senal_actualizar_animacion.emit(rutas_movimiento)
        self.moverse()

    def moverse(self):
        '''
        cambia el atributo posicion, llama
         y emite cambiar_posicion
        '''
        print("en moverse")
        if self.moviendo == "up":
            nueva_pos = (self.posicion[0], self.posicion[1] - 3)
        elif self.moviendo == "down":
            nueva_pos = (self.posicion[0], self.posicion[1] + 3)
        elif self.moviendo == "left":
            nueva_pos = (self.posicion[0] - 3, self.posicion[1])
        elif self.moviendo == "right":
            nueva_pos = (self.posicion[0] + 3, self.posicion[1])
        rect = self.rectangulo_juego
        self.label_personaje_posible = self.label_personaje
        self.label_personaje_posible.move(*nueva_pos)
        if rect[0] < nueva_pos[0] < rect[0] + rect[2] and \
            rect[1] < nueva_pos[1] < rect[1] + rect[3]:
            ########
            obstaculizado = False
            rect_personaje = self.label_personaje_posible.geometry()
            for obstaculo in self.labels_obstaculos:
                rect_obstaculo = obstaculo.geometry()
                if rect_personaje.intersects(rect_obstaculo):
                    obstaculizado = True
            if not obstaculizado:
                self.posicion = nueva_pos
                self.senal_mover_personaje.emit(self.posicion)

    def animacion(self):
        print("animación")
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



    def aviso_no_vida(self):
        '''
        Avisa con una señal que al personaje no le queda vida
        '''

        

class Homero(Personaje):
    def __init__(self) -> None:
        self.nombre = "homero"
        super().__init__()

class Lisa(Personaje):
    def __init__(self) -> None:
        self.nombre = "lisa"
        super().__init__()

class Krusty(Personaje):
    def __init__(self) -> None:
        self.nombre = "krusty"
        super().__init__()

class Moe(Personaje):
    def __init__(self) -> None:
        self.nombre = "moe"
        super().__init__()

class Gorgory(Personaje):
    def __init__(self) -> None:
        self.nombre = "gorgory"
        super().__init__()