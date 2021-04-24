from parametros import DINERO_INICIAL, COSTO_DESENCALLAR, PROB_BASE_DESENCALLAR
from parametros import PONDERADOR_AVANZADO, PONDERADOR_PRINCIPIANTE
from parametros import COBRO_USO_AVANZADO, COBRO_USO_PRINCIPIANTE
from random import randint
from funciones_utiles import ocurre_evento_por_probabilidad
from barcos import ordenar_por_km
from currency_converter import CurrencyConverter
# Info de librería extraída de https://pypi.org/project/CurrencyConverter/

class Canal():
    def __init__(self, nombre, largo, dificultad):
        self.nombre = nombre
        self.dinero = DINERO_INICIAL
        self.largo = largo
        self.barcos = []
        # Contadores de eventos
        self.dinero_gastado = 0
        self.dinero_recibido = 0
        self.n_barcos_historicos = 0
        self.n_barcos_encallados = 0
        self.horas_simuladas = 0
        self.n_eventos_especiales = 0
        # Fin contadores
        self.dificultad = dificultad
        if self.dificultad == "principiante":
            self.ponderador_dificultad = PONDERADOR_PRINCIPIANTE
            self.cobro_de_uso = COBRO_USO_PRINCIPIANTE
        elif self.dificultad == "avanzado":
            self.ponderador_dificultad = PONDERADOR_AVANZADO
            self.cobro_de_uso = COBRO_USO_AVANZADO

    #def barcos():
    #    nombres_barcos = []
    #    for barco in self.__barcos:
    #        nombres_barcos.append(barco.nombre)
    #    return nombres_barcos

    def ingresar_barco(self, barco):
        # Revisar que no debe haber ningún barco encallado
        self.barcos.append(barco)
        barco.km = 0
        barco.tiempo_en_canal = 0
        barco.ponderador_dificultad = self.ponderador_dificultad
        self.n_barcos_historicos += 1
        print(f"El barco {barco.nombre} ingresó al canal")

    def avanzar_barcos(self):
        # simula nueva hora
        # Revisa si el barco está encallado en su atributo
        # Para saber cuánto se desplaza, usa la función desplazar de barco
        # Es llamada por simular_hora.py, acc_simular_hora()
        km_encallamiento = -1
        self.barcos.sort(key=ordenar_por_km, reverse=False)
        for barco in self.barcos:
            if barco.esta_encallado:
                km_encallamiento = barco.km
        if km_encallamiento != -1:
            print(f"La retención más preocupante está en {km_encallamiento}")
        for barco in self.barcos:
            if barco.km > km_encallamiento:
                avanzada = barco.desplazar(self)
                barco.km += avanzada
                if avanzada > 0:
                    print(f"El barco {barco.nombre} avanzó hasta el km {barco.km}")
                else:
                    print(f"El barco {barco.nombre} se quedó en el km {barco.km}")

            # Vemos quién paga a quién
            # Primero el caso cuando sale del canal
            if barco.km >= self.largo:
                self.barcos.sort(key=ordenar_por_km, reverse=False)
                self.barcos.pop()
                self.dinero += self.cobro_de_uso
                self.dinero_recibido += self.cobro_de_uso
                print(f"El barco {barco.nombre} salió del canal y pagó ${self.cobro_de_uso}USD")
            # Ahora el caso en que se mantiene en el canal
            else:
                costo = barco.costo_mantencion
                moneda = barco.moneda_origen
                costo_usd = CurrencyConverter().convert(costo, moneda, "USD")
                self.dinero -= costo_usd
                self.dinero_gastado += costo_usd
                print(f"Se le pagó una mantención de {costo_usd} a {barco.nombre}\n")
                
    def desencallar_barco(self, barco):
        costo = COSTO_DESENCALLAR
        self.dinero_gastado += costo
        self.dinero -= costo
        prob_exito = self.ponderador_dificultad * PROB_BASE_DESENCALLAR
        exito = ocurre_evento_por_probabilidad(prob_exito)
        if exito:
            barco.esta_encallado = False
            return True
        elif not exito:
            return False
