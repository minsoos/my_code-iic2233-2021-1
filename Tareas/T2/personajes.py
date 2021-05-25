from abc import ABC
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QEventLoop, Qt
import parametros as p
from os import path

class Personaje(QObject):

    senal_cambiar_aspecto = pyqtSignal()
    senal_actualizar_animacion= pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.__vida = 1
        self.__moviendo = "up"
        self.moviendo = "up"
        self.transicion_animacion = "3"
        self.velocidad = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.animacion)
        self.timer.setInterval(1000*0.1)
        self.ruta_personajes = p.RUTA_PERSONAJES
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

    @property
    def moviendo(self):
        return self.__moviendo

    @moviendo.setter
    def moviendo(self, movimiento):
        '''
        envía la señal cambiar aspecto según se modifique
        self.__moviendo.
        '''

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
        nuevo_label = path.join(self.ruta_personajes[self.nombre], archivo)
        self.senal_actualizar_animacion.emit(nuevo_label)



    def aviso_no_vida(self):
        '''
        Avisa con una señal que al personaje no le queda vida
        '''

    def recibidor_de_mover(self, movimiento):
        '''
        recibe una tecla apretada, si está entre wasd modifica
        self.moviendo, sino, no hace nada
        '''
        print("recibidor de mover")
        if movimiento != self.__moviendo:
            self.__moviendo = movimiento
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
            ruta_movimiento = path.join(self.ruta_personajes[self.nombre], imagen)
            self.senal_actualizar_animacion.emit(ruta_movimiento)

class Homero(Personaje):
    def __init__(self) -> None:
        self.nombre = "homero"
        super().__init__()

class Lisa(Personaje):
    def __init__(self) -> None:
        self.nombre = "lisa"
        super().__init__()