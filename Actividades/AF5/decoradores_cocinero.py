from funciones import encontrar_preferencia, log


# Debes completar este archivo

def improvisar_toppings(metodo_original):
    def wrapper(self, ingrediente, torta):
        stock = self.ingredientes_disponibles
        if stock[ingrediente] > 0:
            metodo_original(ingrediente, torta)
        else:
            ingrediente_nuevo = encontrar_preferencia(ingrediente)
            print(f"falta {ingrediente}, usaremos {ingrediente_nuevo}")
            metodo_original(ingrediente_nuevo, torta)
    return wrapper

def capa_relleno(tipo_relleno):
    def decorador(metodo_original):
        def wrapper(self, nombre_ingrediente, torta):
            if self.relleno_restante > 1:
                print("queda relleno")
                metodo_original(nombre_ingrediente, torta)
                self.relleno_restante -= 1
            else:
                self.relleno_restante -= 1
                print("se acabó el relleno")

    return decorador


def revisar_ingredientes(metodo_original):
    """
    Este decorador revisa que hayan suficientes ingredientes antes de empezar una torta.
    En caso contrario, debe levantar una excepción del tipo ValueError
    """
    pass
