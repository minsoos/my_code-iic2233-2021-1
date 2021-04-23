from abc import ABC, abstractmethod


class Tripulante(ABC):

    def __init__(self, nombre, experiencia):
        self.nombre = nombre
        self.experiencia = experiencia
    
    @abstractmethod
    def efecto_especial():
        pass


class DCCapitan(Tripulante):

    def __init__(self, nombre, experiencia):
        super().__init__(nombre, experiencia)
        puede_usar_efecto = True

    def efecto_especial():
        ##  desencalla
        puede_usar_efecto = False


class DCCocinero(Tripulante):

    def __init__(self, nombre, experiencia):
        super().__init__(nombre, experiencia)
        puede_usar_efecto = True

    def efecto_especial():
        ##  duplica tiempo de expiracion
        puede_usar_efecto = False


class DCCarguero(Tripulante):

    def __init__(self, nombre, experiencia):
        super().__init__(nombre, experiencia)
        puede_usar_efecto = True

    def efecto_especial():
        ##  aumenta la carga máxima del barco
        puede_usar_efecto = False