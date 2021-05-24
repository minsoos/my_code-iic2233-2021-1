from abc import ABC

class Personaje(ABC):

    senal_cambiar_aspecto = pyqtSignal()

    def __init__(self) -> None:
        self.__vida = 1
        self.__moviendo = None
        self.moviendo = "w"
        self.velocidad = None

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

    def aviso_no_vida(self):
        '''
        Avisa con una señal que al personaje no le queda vida
        '''

    def tecla_apretada(self, tecla):
        '''
        recibe una tecla apretada, si está entre wasd modifica
        self.moviendo, sino, no hace nada
        '''

class Homero(Personaje):
    def __init__(self) -> None:
        super().__init__()

class Lisa(Personaje):
    def __init__(self) -> None:
        super().__init__()