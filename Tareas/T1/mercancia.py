from parametros import MULTA_PETROLEO, MULTA_ALIMENTOS, MULTA_ROPA

class Mercancia:
    def __init__(self, numero, tipo, tiempo_expiracion, peso):
        self.numero = numero
        self.tipo = tipo
        self.tiempo_expiracion = tiempo_expiracion
        self.peso = peso
    
    def expirar(barco):
        if barco.tiempo_en_canal > self.tiempo_expiracion:
            #  Vemos cuál es la multa
            if self.tipo = "petroleo":
                multa = MULTA_PETROLEO
            if self.tipo = "ropa":
                multa = MULTA_ROPA
            if self.tipo = "alimentos":
                multa = MULTA_ALIMENTOS
            return (True, multa)
        else:
            return (False, 0)