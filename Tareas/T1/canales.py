from parametros import DINERO_INICIAL, COSTO_DESENCALLAR, PROB_BASE_DESENCALLAR
from parametros import PONDERADOR_AVANZADO, PONDERADOR_PRINCIPIANTE

class Canal():
    def __init__(self, nombre, largo, dificultad):
        self.nombre = nombre
        self.dinero = DINERO_INICIAL
        self.cobro_de_uso = cobro_de_uso
        self.largo = largo
        self.__barcos = []
        self.agregaste_un_barco_esta_hora = False
        self.dificultad = dificultad
        if self.dificultad = "":
            self.ponderador_dificultad = PONDERADOR_PRINCIPIANTE
        elif self.dificultad = "":
            self.ponderador_dificultad = PONDERADOR_AVANZADO

    @property
    def dificultad():
        

    @property
    def barcos():
        nombres_barcos = []
        for barco in self.__barcos:
            nombres_barcos.append(barco.nombre)
        return nombres_barcos

    def ingresar_barco_al_canal(barco):
        if self.agregaste_un_barco_esta_hora == False:
            if barco not in self.__barcos:
                self.__barcos.append(barco)
                self.agregaste_un_barco_esta_hora = True
    
    def avanzar_barcos():
        ##simula nueva hora
        self.agregaste_un_barco_esta_hora = False

    def desencallar_barco():
        costo = COSTO_DESENCALLAR
        prob_exito = self.ponderador_dificultad * PROB_BASE_DESENCALLAR


    