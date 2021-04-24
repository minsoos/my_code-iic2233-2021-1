from parametros import DINERO_INICIAL, COSTO_DESENCALLAR, PROB_BASE_DESENCALLAR
from parametros import PONDERADOR_AVANZADO, PONDERADOR_PRINCIPIANTE
from parametros import COBRO_USO_AVANZADO, COBRO_USO_PRINCIPIANTE
from random import randint
from funciones_utiles import ocurre_evento_por_probabilidad


class Canal():
    def __init__(self, nombre, largo, dificultad):
        self.nombre = nombre
        self.dinero = int(DINERO_INICIAL)
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
        self.agregaste_un_barco_esta_hora = False
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

    def ingresar_barco_al_canal(self, barco):
        if not self.agregaste_un_barco_esta_hora:
            self.barcos.append(barco)
            barco.km = 0
            self.agregaste_un_barco_esta_hora = True
            self.n_barcos_historicos += 1

    def avanzar_barcos(self, ):
        ##simula nueva hora
        # Revisa si el barco está encallado en su atributo
        # Para saber cuánto se desplaza, usa la función desplazar de barco
        self.agregaste_un_barco_esta_hora = False

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




    