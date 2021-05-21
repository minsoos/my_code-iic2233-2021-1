from funciones import encontrar_preferencia, log


# Debes completar este archivo

def improvisar_toppings(metodo_original):
    def wrapper(self, ingrediente, torta):
        stock = self.ingredientes_disponibles
        ingrediente_nuevo = ingrediente
        while stock[ingrediente_nuevo] < 1:
            ingrediente_nuevo = encontrar_preferencia(ingrediente)
        if ingrediente_nuevo != ingrediente:
            log(f"falta {ingrediente}, usaremos {ingrediente_nuevo}", "ingredientes")
        metodo_original(self, ingrediente_nuevo, torta)
    return wrapper

def capa_relleno(tipo_relleno):
    def decorador(metodo_original):
        def wrapper(self, nombre_ingrediente, torta):
            if self.relleno_restante > 0:
                torta.append(tipo_relleno)
                log("queda relleno", "relleno")
                metodo_original(self, nombre_ingrediente, torta)
                self.relleno_restante -= 1
            else:
                log("se acabó el relleno", "relleno")
                torta.finalizada = True
        return wrapper

    return decorador


def revisar_ingredientes(metodo_original):
    def wrapper(self, nombre, lista_ingredientes):
        n_ingredientes_totales = 0
        for i in self.ingredientes_disponibles:
            n_ingredientes_totales += self.ingredientes_disponibles[i]
        if n_ingredientes_totales < len(lista_ingredientes):
            log("no hay suficientes ingredientes", "ingredientes")
            raise ValueError("no hay suficientes ingredientes")
        else:
            return metodo_original(self, nombre, lista_ingredientes)
    return wrapper
