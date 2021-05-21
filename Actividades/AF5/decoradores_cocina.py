from funciones import desencriptar, encriptar, log
from random import uniform


def desencriptar_receta(metodo_original):
    def wrapper(self, archivo):
        diccionario_encriptado = metodo_original(self, archivo)
        for receta in diccionario_encriptado:
            ingredientes_aux = diccionario_encriptado[receta]
            for ingrediente_i in range(len(ingredientes_aux)):
                ingredientes_aux[ingrediente_i] = desencriptar(ingredientes_aux[ingrediente_i])

        return diccionario_encriptado
    return wrapper


def encriptar_receta(metodo_original):
    def wrapper(self, receta):
        for palabra in range(len(receta)):
            receta[palabra] = encriptar(receta[palabra])
        metodo_original(self, receta)
    return wrapper


def ingredientes_infectados(probabilidad_infectado):
    def decorador(metodo_original):
        """
        Este decorador debe hacer que el método "revisar_despensa" elmine los ingredientes
        que pueden estar infectados, según la probabilidad dada.
         """
        def wrapper(self, archivo):
            diccionario_despensa = metodo_original(self, archivo)
            for ingrediente in diccionario_despensa:
                n_comparar = uniform(0, 1)
                if n_comparar < probabilidad_infectado:
                    diccionario_despensa[ingrediente] = 1
                    log(f"{ingrediente} infectado", "ingredientes")
            return diccionario_despensa
        return wrapper
    return decorador
