from parametros import DINERO_INICIAL, COSTO_DESENCALLAR, PROB_BASE_DESENCALLAR
from parametros import PONDERADOR_AVANZADO, PONDERADOR_PRINCIPIANTE
from parametros import COBRO_USO_AVANZADO, COBRO_USO_PRINCIPIANTE
class Canal():
    def __init__(self, nombre, largo, dificultad):
        self.nombre = nombre
        self.dinero = DINERO_INICIAL
        self.largo = largo
        self.barcos = []
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
        if self.agregaste_un_barco_esta_hora == False:
            self.barcos.append(barco)
            self.agregaste_un_barco_esta_hora = True
    
    def avanzar_barcos(self, ):
        ##simula nueva hora
        self.agregaste_un_barco_esta_hora = False

    def desencallar_barco(self, barco):
        costo = COSTO_DESENCALLAR
        prob_exito = self.ponderador_dificultad * PROB_BASE_DESENCALLAR


    