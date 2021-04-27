from parametros import MULTA_PETROLEO, MULTA_ALIMENTOS, MULTA_ROPA


class Mercancia:
    def __init__(self, numero, tipo, tiempo_expiracion, peso):
        self.numero = numero
        self.tipo = tipo
        self.tiempo_expiracion = tiempo_expiracion
        self.peso = peso
        self.tiempo = 0
        self.caducado = False

    def expirar(self):
        if self.tipo == "petróleo":
            multa = MULTA_PETROLEO
        if self.tipo == "ropa":
            multa = MULTA_ROPA
        if self.tipo == "alimentos":
            multa = MULTA_ALIMENTOS
        return multa

    def pasa_una_hora(self):
        self.tiempo += 1
        if self.tiempo > self.tiempo_expiracion and not self.caducado:
            print(f"Caducó la mercancía {self.numero}, que es {self.tipo}")
            self.caducado = True
            return self.expirar()
        else:
            return 0
