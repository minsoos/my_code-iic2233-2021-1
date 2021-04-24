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
        self.ponderador_dificultad = None

    def desplazar(self, canal):
        peso_mercancia = 0
        for caja in self.mercancia:
            peso_mercancia += caja.peso
        min_1 = (self.carga_maxima - peso_mercancia - 0.3*self.pasajeros)/self.carga_maxima
        desplazamiento = max(0.1, min(1, min_1))*self.velocidad_base
        # El valor retornado retorna a la simulación
        # Es la simulación la que tiene que comprobar qué barcos pueden avanzar o no
        #
        multa_total = 0
        for caja in self.mercancia:
            multa = caja.pasa_una_hora()
            multa_total += multa
        canal.dinero -= multa_total
        canal.dinero_gastado += multa_total
        if multa_total != 0:
            print(f"El canal pagó una multa de {multa_total} a {self.nombre} por mercancía caducada")
        #
        if self.encallar(canal.dificultad):
            print(f"El barco {self.nombre} lamentablemente encalló")
            canal.n_barcos_encallados
            return 0
        else:
            self.evento_especial()
            return desplazamiento
        print("")
    
    def encallar(self, dificultad_canal):
        # Se usa sólo en la función desplazar
        prob_encallar = self.prob_encallar
        ocurre = ocurre_evento_por_probabilidad(prob_encallar)
        # Esto está mal, falta la dificultad del canal
        if ocurre:
            self.esta_encallado = True
            return True
        else:
            return False
    
    @property
    def prob_encallar(self):
        exp_acumulada = 0
        for tripulante in self.tripulacion:
            exp_acumulada += tripulante.experiencia
        mercancia_acumulada = 0
        for caja in self.mercancia:
            mercancia_acumulada += caja.peso
        min_1 = (self.velocidad_base + mercancia_acumulada - exp_acumulada)/120
        self.__prob_encallar = min(1, min_1) * self.tend_encallar * self.ponderador_dificultad
        return self.__prob_encallar
    
    @abstractmethod
    def evento_especial(self):
        pass


class BarcoPasajeros(Barco):
    def __init__(self, diccionario):
        super().__init__(diccionario)
        self.tend_encallar = parametros.TENDENCIA_ENCALLAR_PASAJEROS
        self.__prob_encallar = None
    
    def evento_especial(self):
        # Puedo meter al canal como argumento?
        pass


class BarcoCarguero(Barco):
    def __init__(self, diccionario):
        super().__init__(diccionario)
        self.tend_encallar = parametros.TENDENCIA_ENCALLAR_CARGUERO
        self.__prob_encallar = None

    def evento_especial(self):
        pass


class Buque(Barco):
    def __init__(self, diccionario):
        super().__init__(diccionario)
        self.tend_encallar = parametros.TENDENCIA_ENCALLAR_BUQUE
        self.__prob_encallar = None

    def evento_especial(self):
        pass


#def probabilidad_encallar_barco(barco, canal):
#    exp_acumulada = 0
#        for tripulante in barco.tripulacion:
#            exp_acumulada += tripulante.experiencia
#       min_1 = (barco.velocidad_base + barco.mercancia - exp_acumulada)/120
#        barco.prob_encallar = min(1, min_1) * barco.tend_encallar * canal.dificultad_canal
#        return prob_encallar

def ordenar_por_km(barco):
    return barco.km


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
    print(mi_barco.prob_encallar)