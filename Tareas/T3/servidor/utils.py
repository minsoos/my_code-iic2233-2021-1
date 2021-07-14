from os import path
import json


def normalizar_ruta(ruta):
    lista = ruta.split("/")
    path_ = path.join(*lista)
    return path_


def cargar_parametros(ruta=path.join("parametros.json")):
    diccionario_parametros = dict()
    with open(ruta, encoding='utf-8') as archivo:
        diccionario_parametros = json.load(archivo)
    return diccionario_parametros


class Nodo:

    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.caminos = []

    def agregar_camino(self, nodo, costo):
        camino = Camino(self, nodo, costo)
        self.caminos.append(camino)
        nodo.caminos.append(camino)
    
    def dfs_search_nodo(self, nombre_nodo, visitados=None):
        visitados = visitados or set()

        visitados.add(self)

        for camino in self.caminos:
            vecino = camino.nodo_1 if camino.nodo_1 != self else camino.nodo2
            if vecino not in visitados:
                if vecino.nombre == nombre_nodo:
                    return vecino
                vecino.dfs_search(nombre_nodo, visitados)
    
    def dfs_search_lista_nodos(self, visitados=None):
        visitados = visitados or set()

        visitados.add(self)

        for camino in self.caminos:
            vecino = camino.nodo_1 if camino.nodo_1 != self else camino.nodo_2
            if vecino not in visitados:
                vecino.dfs_search_lista_nodos(visitados)
        return visitados



class Camino:

    def __init__(self, nodo_1, nodo_2, costo):
        self.nodo_1 = nodo_1
        self.nodo_2 = nodo_2
        self.costo = costo
        self.dueno = None

    def comprar_camino(self, comprador):
        if self.dueno is None:
            self.dueno = comprador
            return True
        else:
            return False


def crear_mapa(ruta="mapa.json", mapa="ingenieria"):
    with open(ruta, encoding='utf-8') as archivo:
        diccionario = json.load(archivo)

    if mapa == "ingenieria":
        key_mapa = "ingenieria"
    elif mapa == "san joaquin":
        key_mapa = "san_joaquin"
    else:
        raise ValueError("El mapa ingresado no está en las opciones")
    diccionario_puntos = diccionario["mapa"][key_mapa]["posiciones"]
    diccionario_caminos = diccionario["mapa"][key_mapa]["caminos"]

    for punto in diccionario_puntos:
        x = diccionario_puntos[punto]["x"]
        y = diccionario_puntos[punto]["y"]
        diccionario_puntos[punto] = Nodo(punto, x, y)

    for punto in diccionario_caminos:
        for camino in diccionario_caminos[punto]:
            nodo_1 = diccionario_puntos[punto]
            nodo_2 = diccionario_puntos[camino[0]]
            presio = camino[1]
            crear = True
            for camino in nodo_1.caminos:
                if camino.nodo_1 == nodo_2 or camino.nodo_2 == nodo_2:
                    crear = False
            if crear:
                diccionario_puntos[punto].agregar_camino(nodo_2, presio)

    return diccionario_puntos