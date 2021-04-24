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
        self.__puede_usar_efecto = True
        self.tipo = "DCCapitan"
    
    def efecto_especial():
        ##  desencalla
        self.__puede_usar_efecto = False


class DCCocinero(Tripulante):

    def __init__(self, nombre, experiencia):
        super().__init__(nombre, experiencia)
        self.__puede_usar_efecto = True
        self.tipo = "DCCocinero"
    
    def efecto_especial():
        ##  duplica tiempo de expiracion
        self.__puede_usar_efecto = False


class DCCarguero(Tripulante):

    def __init__(self, nombre, experiencia):
        super().__init__(nombre, experiencia)
        self.__puede_usar_efecto = True
        self.tipo = "DCCarguero"
    
    def efecto_especial():
        ##  aumenta la carga máxima del barco
        self.__puede_usar_efecto = False