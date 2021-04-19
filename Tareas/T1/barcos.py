from abc import ABC, abstractmethod
class Barco(ABC):
    def __init__(self, nombre, costo_mantencion, velocidad_base, **kargs):
        self.nombre = nombre
        self.costo_mantencion = costo_mantencion
        self.velocidad_base = velocidad_base
        self.pasajeros = pasajeros
        self.carga_maxima = carga_maxima
        self.moneda_origen = moneda_origen
        self.prob_encallar = prob_encallar
        self.tripulacion = tripulacion
        self.mercancia = mercancia

    def desplazar(self):
        min_1 = (self.carga_maxima - self.mercancia - 0.3*self.pasajeros)/self.carga_maxima
        desplazamiento = max(0.1, min(1, min_1))*self.velocidad_base
        return desplazamiento

    def encallar(self):
        exp_acumulada = 0
        for tripulante in self.tripulacion:
            tripulante.exp  ##  rellenar
        min_1 = (self.velocidad_base + self.mercancia - exp_acumulada)/120
        prob_encallar = min(1, min_1)* pass #  rellenar

    @abstractmethod
    def evento_especial(self):
        pass


class BarcoPasajeros(Barco):
    def __init__(self, nombre, costo_mantencion, velocidad_base, **kargs):
        super().__init__(nombre, costo_mantencion, velocidad_base, **kargs)
        self.tend_encallar = TENDENCIA_ENCALLAR_PASAJEROS

    def evento_especial(self):
        pass



class BarcoCarguero(Barco):
    def __init__(self, nombre, costo_mantencion, velocidad_base, **kargs):
        super().__init__(nombre, costo_mantencion, velocidad_base, **kargs)
        self.tend_encallar = TENDENCIA_ENCALLAR_CARGUERO

    def evento_especial(self):
        pass



class Buque(Barco):
    def __init__(self, nombre, costo_mantencion, velocidad_base, **kargs):
        super().__init__(nombre, costo_mantencion, velocidad_base, **kargs)
        self.tend_encallar = TENDENCIA_ENCALLAR_BUQUE

    def evento_especial(self):
        pass
