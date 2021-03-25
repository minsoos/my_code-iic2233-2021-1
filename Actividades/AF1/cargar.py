from collections import namedtuple, defaultdict


def cargar_platos(ruta_archivo = "platos.csv"):
    archivo = open(ruta_archivo)
    lista_de_platos = archivo.readlines()
    Plato = namedtuple("platos", ["categoria", "tiempo_preparacion", "precio", "ingredientes"])
    diccionario_de_platos = dict()
    for i in range(len(lista_de_platos)):
        lista_de_platos[i] = lista_de_platos[i].strip().split(",")
        plato = lista_de_platos[i]
        tupla_aux = Plato(plato[1], int(plato[2]), int(plato[3]), set(plato[4:len(plato)]))
        diccionario_de_platos[plato[0]] = tupla_aux
    return diccionario_de_platos


def cargar_ingredientes(ruta_archivo = "ingredientes.csv"):
    archivo = open(ruta_archivo)
    lista_ingredientes = archivo.readlines()
    diccionario_ingredientes = dict()
    for i in range(len(lista_ingredientes)):
        lista_ingredientes[i] = lista_ingredientes[i].strip().split(",")
        ingr = lista_ingredientes[i]
        diccionario_ingredientes[ingr[0]] = int(ingr[1])
    return diccionario_ingredientes


if __name__ == "__main__":
    # ================== PUEDES PROBAR TUS FUNCIONES AQUÍ =====================
    print(" PRUEBA CARGAR ".center(80, "="))
