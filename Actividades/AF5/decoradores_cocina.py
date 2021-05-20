from funciones import desencriptar, encriptar, log
from random import uniform


def desencriptar_receta(metodo_original):
    def wrapper(*args, **kwargs):
        diccionario_encriptado = metodo_original()
        for receta in diccionario_encriptado:
            ingredientes_aux = diccionario_encriptado[receta]
            for ingrediente_i in range(len(ingredientes_aux)):
                ingredientes_aux[ingrediente_i] = desencriptar(ingredientes_aux[ingrediente_i])

        return diccionario_encriptado
    return wrapper


def encriptar_receta(metodo_original):
    def wrapper(self, receta):
        receta = encriptar(receta)
        retorno = metodo_original(receta)
        return retorno
    return wrapper


def ingredientes_infectados(probabilidad_infectado):
    def decorador(metodo_original):
        """
        Este decorador debe hacer que el método "revisar_despensa" elmine los ingredientes
        que pueden estar infectados, según la probabilidad dada.
         """
        def wrapper(self, archivo):
            diccionario_despensa = metodo_original(archivo)
            n_comparar = uniform(0,1)
            for ingrediente in diccionario_despensa:
                if n_comparar < probabilidad_infectado:
                    diccionario_despensa[ingrediente] = 1
                    print(f"{ingrediente} infectado")
            return diccionario_despensa
        return wrapper
    return decorador
