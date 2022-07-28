from collections import deque
import parametros as p


# Funciones que revisan todos los nodos para desmantelar la organización


def recorrer_mafia(inicio):
    # COMPLETAR
    lugares_lideres = []
    bfs(inicio, lugares_lideres)
    return lugares_lideres
    

def bfs(inicio, lugares_lideres):
    visitados = []
    por_visitar = deque([inicio])
    visitados.append(inicio)
    while len(por_visitar) > 0:
        lugar_actual = por_visitar.popleft()
        print(lugar_actual.nombre)
        for conexion in lugar_actual.conexiones:
            lugar_vecino = conexion.vecino
            if lugar_vecino not in visitados:
                por_visitar.append(lugar_vecino)
                visitados.append(lugar_vecino)

        print(f"Se ha desmantelado {lugar_actual.nombre}")
        for mafioso in lugar_actual.mafiosos:
            if mafioso.frase == p.frase_lider_1 or\
                mafioso.frase == p.frase_lider_2:
                lugares_lideres.append(lugar_actual)

# BONUS
# Recibe como inicio el nodo en el que está uno de los líderes de la mafia
# y como termino el nodo en el que esta el otro lider

def bfs_modificado(inicio):
    visitados = []
    por_visitar = deque([inicio])
    visitados.append(inicio)
    while len(por_visitar) > 0:
        lugar_actual = por_visitar.popleft()
        print(lugar_actual.nombre)
        for conexion in lugar_actual.conexiones:
            lugar_vecino = conexion.vecino
            if lugar_vecino not in visitados:
                por_visitar.append(lugar_vecino)
                visitados.append(lugar_vecino)
    return visitados


def minima_peligrosidad(inicio, termino):
    distancias = {}
    nodos_posibles = bfs_modificado(inicio)
    for nodo in nodos_posibles:
        distancias[nodo] = float("Inf")
    distancias[inicio] = 0
    distancias[termino] = float("Inf")
    nodos_out = set()
    otra_funcion(inicio, distancias, nodos_out)
    return distancias[termino]

def otra_funcion(actual, distancias, nodos_out):
    for conexion in actual.conexiones:
        nuevo_peso = distancias[actual] + conexion.peso
        if nuevo_peso < distancias[conexion.vecino]:
            distancias[conexion.vecino.nombre] = nuevo_peso
    nodos_out.add(actual)

    if len(nodos_out) < len(distancias.keys()):
        for nodo in distancias:
            if distancias[nodo] not in nodos_out:
                otra_funcion(actual, distancias, nodos_out)
            
