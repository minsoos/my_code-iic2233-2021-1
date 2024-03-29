import cargar_archivos as c
from collections import namedtuple


class NodoLugar:
    # NO MODIFICAR
    def __init__(self, nombre):
        self.nombre = nombre
        # Lista de namedtuples del tipo mafioso (definido en cargar_archivos.py)
        self.mafiosos = []
        # Lista de namedtuples del tipo conexion, con los atributos vecino
        # y peso, que guardan el nodo vecino y el peso de dicha conexion
        self.conexiones = []

    def agregar_conexion(self, destino, peso):
        Conexion = namedtuple("Conexion", ["vecino", "peso"])
        self.conexiones.append(
            Conexion(vecino=destino, peso=peso)
        )

    def __str__(self):
        # Puedes imprimir el nodo :D
        texto = ""
        nombres = ", ".join([habitante.nombre for habitante in self.mafiosos])
        texto += f"En {self.nombre} se encuentran los mafiosos {nombres}.\n"
        conexiones = ", ".join([f"{conexion.vecino.nombre} de peso {conexion.peso}"
                                for conexion in self.conexiones])
        texto += f"Desde aqui puedes ir a {conexiones}.\n"
        return texto


def crear_grafo(dic_lugares, conexiones):
    # COMPLETAR
    # Crea los nodos, teniendo en cuenta sus mafiosos, las conexiones y sus pesos
    dict_nodos = {}
    for lugar in dic_lugares:
        nodo = NodoLugar(lugar)
        nodo.mafiosos = dic_lugares[lugar]
        dict_nodos[nodo.nombre] = nodo
    for conexion in conexiones:
        dict_nodos[conexion[0]].agregar_conexion(dict_nodos[conexion[1]], conexion[2])
        dict_nodos[conexion[1]].agregar_conexion(dict_nodos[conexion[0]], conexion[2])
    return nodo


if __name__ == "__main__":
    # Puedes usar esta parte para probar tu avance
    pass
