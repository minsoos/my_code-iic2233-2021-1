from collections import namedtuple, defaultdict


def cargar_platos(ruta_archivo = "platos.csv"):
    archivo = open(ruta_archivo)
    lista_de_platos = archivo.readlines()
    Plato = namedtuple("platos", ["n", "categoria", "tiempo", "precio", "ingredientes"])
    diccionario_de_platos = dict()
    for i in range(len(lista_de_platos)):
        lista_de_platos[i] = lista_de_platos[i].strip().split(",")
        p = lista_de_platos[i]
        tupla_aux = Plato(p[0], p[1], int(p[2]), int(p[3]), set(p[4:len(p)]))
        diccionario_de_platos[p[0]] = tupla_aux
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
    cargar_ingredientes()
    platoscargados = cargar_platos()
    for i in platoscargados:
        print("ssd",platoscargados[i].categoria)