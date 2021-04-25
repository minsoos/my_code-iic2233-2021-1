from abc import ABC, abstractmethod
import parametros

class Tripulante(ABC):

    def __init__(self, nombre, experiencia):
        self.nombre = nombre
        self.experiencia = experiencia
    
    @abstractmethod
    def efecto_especial(self):
        pass


class DCCapitan(Tripulante):

    def __init__(self, nombre, experiencia):
        super().__init__(nombre, experiencia)
        self.puede_usar_efecto = True
        self.tipo = "DCCapitán"

    def efecto_especial(self, barco):
        if barco.esta_encallado and self.puede_usar_efecto:
            barco.esta_encallado = False
            self.puede_usar_efecto = False
            return True
        else:
            return False


class DCCocinero(Tripulante):

    def __init__(self, nombre, experiencia):
        super().__init__(nombre, experiencia)
        self.tipo = "DCCocinero"

    def efecto_especial(self, barco):
        for caja in barco.mercancia:
            if caja.tipo == "alimentos":
                caja.tiempo_expiracion = caja.tiempo_expiracion * 2


class DCCarguero(Tripulante):

    def __init__(self, nombre, experiencia):
        super().__init__(nombre, experiencia)
        self.tipo = "DCCarguero"

    def efecto_especial(self, barco):
        barco.carga_maxima += parametros.CARGA_EXTRA_CARGUERO
