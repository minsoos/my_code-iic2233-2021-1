from abc import ABC, abstractmethod
import parametros
from funciones_utiles import ocurre_evento_por_probabilidad, ordenar_por_km


class Barco(ABC):
    def __init__(self, diccionario):
        self.nombre = diccionario["nombre"]
        self.costo_mantencion = diccionario["costo_mantencion"]
        self.velocidad_base = diccionario["velocidad_base"]
        self.pasajeros = diccionario["pasajeros"]
        self.carga_maxima = diccionario["carga_maxima"]
        self.moneda_origen = diccionario["moneda_origen"]
        # La relación de composición de tripulación se establece en la carga de archivos,
        # la cual no permite que existan barcos con menos de un tripulante
        # (ni por enunciado más de 3)
        self.tripulacion = diccionario["tripulacion"]
        self.mercancia = diccionario["mercancia"]
        self.esta_encallado = False
        self.__prob_encallar = None
        # Los siguientes atributos son seteados por el método ingresar_barco de Canal
        self.tiempo_en_canal = 0
        self.km = 0
        self.ponderador_dificultad = None

    def desplazar(self, canal):
        peso_mercancia = 0
        for caja in self.mercancia:
            peso_mercancia += caja.peso
        min_1 = (self.carga_maxima - peso_mercancia - 0.3*self.pasajeros)/self.carga_maxima
        desplazamiento = max(0.1, min(1, min_1))*self.velocidad_base
        # El valor retornado retorna a la simulación
        # Es la simulación la que tiene que comprobar qué barcos pueden avanzar o no
        # Calculamos la multa de los alimentos vencidos
        multa_total = 0
        for caja in self.mercancia:
            multa = caja.pasa_una_hora()
            multa_total += multa
        canal.dinero -= multa_total
        canal.dinero_gastado += multa_total
        if multa_total != 0:
            print(f"Se pagó una multa de {multa_total} a {self.nombre} por mercancía caducada")
        #
        encalla = self.encallar()
        #Revisamos si podemos usar la habilidad especial del capitán
        if encalla:
            canal.n_barcos_encallados += 1
            for tripulante in self.tripulacion:
                if tripulante.tipo == "DCCapitán":
                    lo_hace = tripulante.efecto_especial(self)
                    if lo_hace:
                        print(f"El capitán valiente de {self.nombre} evitó que encallara el barco")
                        encalla = False
        #
        # Ahora vemos los casos en que encalla y en que no
        if encalla:
            print(f"El barco {self.nombre} lamentablemente encalló")
            return 0
        else:
            self.evento_especial(canal)
            return desplazamiento
        print("")
    
    def encallar(self):
        # Este método se usa sólo en la función desplazar
        prob_encallar = self.prob_encallar
        ocurre = ocurre_evento_por_probabilidad(prob_encallar)
        if ocurre:
            self.esta_encallado = True
            return True
        else:
            return False
    
    @property
    def prob_encallar(self):
        # Este método setea el atributo oculto prob_encallar cada vez que se llama
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
        self.senal_evento_especial = False
        self.tipo = "BarcoPasajeros"

    def evento_especial(self, canal):
        ocurre = ocurre_evento_por_probabilidad(parametros.PROBABILIDAD_EVENTO_ESPECIAL)
        if ocurre and not self.senal_evento_especial:
            print("Ocurrió una intoxicación masiva de los pasajeros")
            print(f"El barco te paga {parametros.DINERO_INTOXICACION} para comprar remedios")
            canal.dinero += parametros.DINERO_INTOXICACION
            canal.dinero_recibido += parametros.DINERO_INTOXICACION
            self.senal_evento_especial = True
            canal.n_eventos_especiales += 1
            return True
        else:
            return False

class BarcoCarguero(Barco):
    def __init__(self, diccionario):
        super().__init__(diccionario)
        self.tend_encallar = parametros.TENDENCIA_ENCALLAR_CARGUERO
        self.senal_evento_especial = False
        self.tipo = "BarcoCarguero"

    def evento_especial(self, canal):
        ocurre = ocurre_evento_por_probabilidad(parametros.PROBABILIDAD_EVENTO_ESPECIAL)
        if ocurre and not self.senal_evento_especial:
            print("El barco fue atacado por piratas! ya no te podrá pagar la salida")
            self.pagar_salida = False
            self.senal_evento_especial = True
            self.mercancia = []
            canal.n_eventos_especiales += 1
            return True
        else:
            return False
            

class Buque(Barco):
    def __init__(self, diccionario):
        super().__init__(diccionario)
        self.tend_encallar = parametros.TENDENCIA_ENCALLAR_BUQUE
        self.averia_buque = 0
        self.senal_evento_especial = False
        self.tipo = "Buque"

    def evento_especial(self, canal):
        ocurre = ocurre_evento_por_probabilidad(parametros.PROBABILIDAD_EVENTO_ESPECIAL)
        if ocurre and not self.senal_evento_especial:
            tiempo = parametros.TIEMPO_AVERIA_BUQUE
            print(f"El buque se averió, deberá quedarse donde está por {tiempo} horas")
            self.averia_buque += tiempo
            self.senal_evento_especial = True
            canal.n_eventos_especiales += 1
            return True
        else:
            return False



#def probabilidad_encallar_barco(barco, canal):
#    exp_acumulada = 0
#        for tripulante in barco.tripulacion:
#            exp_acumulada += tripulante.experiencia
#       min_1 = (barco.velocidad_base + barco.mercancia - exp_acumulada)/120
#        barco.prob_encallar = min(1, min_1) * barco.tend_encallar * canal.dificultad_canal
#        return prob_encallar



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