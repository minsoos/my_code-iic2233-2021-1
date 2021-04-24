from abc import ABC, abstractmethod
import parametros
from funciones_utiles import ocurre_evento_por_probabilidad
class Barco(ABC):
    def __init__(self, diccionario):
        self.nombre = diccionario["nombre"]
        self.costo_mantencion = diccionario["costo_mantencion"]
        self.velocidad_base = diccionario["velocidad_base"]
        self.pasajeros = diccionario["pasajeros"]
        self.carga_maxima = diccionario["carga_maxima"]
        self.moneda_origen = diccionario["moneda_origen"]
        self.tripulacion = diccionario["tripulacion"]
        self.mercancia = diccionario["mercancia"]
        self.tiempo_en_canal = 0
        self.esta_encallado = False
        self.km = None

    def desplazar(self):
        min_1 = (self.carga_maxima - self.mercancia - 0.3*self.pasajeros)/self.carga_maxima
        desplazamiento = max(0.1, min(1, min_1))*self.velocidad_base
        return desplazamiento

    def encallar(self, dificultad_canal):
        ocurre = ocurre_evento_por_probabilidad(self.prob_encallar)
        if ocurre:
            self.esta_encallado = True
        else:
            pass

    @abstractmethod
    def evento_especial(self):
        pass


class BarcoPasajeros(Barco):
    def __init__(self, diccionario):
        super().__init__(diccionario)
        self.tend_encallar = parametros.TENDENCIA_ENCALLAR_PASAJEROS
        self.prob_encallar = probabilidad_encallar_barco(self)
    def evento_especial(self):
        pass



class BarcoCarguero(Barco):
    def __init__(self, diccionario):
        super().__init__(diccionario)
        self.tend_encallar = parametros.TENDENCIA_ENCALLAR_CARGUERO
        self.prob_encallar = probabilidad_encallar_barco(self)

    def evento_especial(self):
        pass



class Buque(Barco):
    def __init__(self, diccionario):
        super().__init__(diccionario)
        self.tend_encallar = parametros.TENDENCIA_ENCALLAR_BUQUE
        self.prob_encallar = probabilidad_encallar_barco(self)

    def evento_especial(self):
        pass

def probabilidad_encallar_barco(barco):
    exp_acumulada = 0
        for tripulante in barco.tripulacion:
            exp_acumulada += tripulante.experiencia
        min_1 = (barco.velocidad_base + barco.mercancia - exp_acumulada)/120
        barco.prob_encallar = min(1, min_1) * barco.tend_encallar * dificultad_canal
        return prob_encallar

if __name__ == "__main__":
    diccionario = {}
    diccionario["nombre"] = "Perro"
    diccionario["costo_mantencion"] = 1.2
    diccionario["velocidad_base"] = 13
    diccionario["pasajeros"] = 12
    diccionario["carga_maxima"] = 34
    diccionario["moneda_origen"] = "sr"
    diccionario["tripulacion"] = []
    diccionario["mercancia"] = []
    print(diccionario)
    mi_barco = Buque(diccionario)