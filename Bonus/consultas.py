import pyrematch as re


# ------------------------------------------------------------------------------------------------
# DEFINIR AQUI LOS PATRONES PARA CONSTRUIR CADA EXPRESION REGULAR
# NO CAMBIAR LOS NOMBRES DE LAS VARIABLES
PATRON_1 = "(^|\n)# !titulo{[^\n]+}($|\n)"
PATRON_2 = "(^|\n)[#]{2,3} !subtitulo{[^\.\n]+}(\n|$)"
PATRON_3 = "(^|\n)<img src='!imagen{[^\n]+}' alt>($|\n)"
PATRON_4 = "(^|\n)```!contenido{[^\n]+}\n!codigo{[^`]+}```($|\n)"
PATRON_5 = "(^|\n)(\*|-) \[(X|x)\] !objeto{[^\n]+}(\n|$)" # No c
PATRON_6 = "(^|\n)!completo{[^\n]*\[[^\n]+\]\(!referencia{[^\n(]+}\)[^\n]*}(\n|$)"


# ------------------------------------------------------------------------------------------------
# Completar a continuación el código de cada consulta. Cada consulta recibe el patrón
# correspondiente para construir la expresión regular, y el texto sobre el cual se aplicará.
# Cada consulta debe retornar una lista de diccionarios, donde cada diccionario contiene dos
# llaves: "contenido" (el texto del match encontrado) y "posicion" (lista con dos elementos: la
# posición de inicio y la posición de término del match encontrado).


# CONSULTA 1
def consulta_1(texto, patron):
    regex = re.compile(patron)
    lista = []
    for match in regex.finditer(texto):
        diccionario = {
            "contenido": match.group("titulo"),
            "posicion": match.span("titulo")
        }
        lista.append(diccionario)
    return lista


# CONSULTA 2
def consulta_2(texto, patron):
    regex = re.compile(patron)
    lista = []
    for match in regex.finditer(texto):
        diccionario = {
            "contenido": match.group("subtitulo"),
            "posicion": match.span("subtitulo")
        }
        lista.append(diccionario)
    return lista


# CONSULTA 3
def consulta_3(texto, patron):
    regex = re.compile(patron)
    lista = []
    for match in regex.finditer(texto):
        diccionario = {
            "contenido": match.group("imagen"),
            "posicion": match.span("imagen")
        }
        lista.append(diccionario)
    return lista


# CONSULTA 4
def consulta_4(texto, patron):
    regex = re.compile(patron)
    lista = []
    for match in regex.finditer(texto):
        diccionario = {
            "contenido": match.group("contenido"),
            "posicion": match.span("codigo")
        }
        lista.append(diccionario)
    return lista


# CONSULTA 5
def consulta_5(texto, patron):
    regex = re.compile(patron)
    lista = []
    for match in regex.finditer(texto):
        diccionario = {
            "contenido": match.group("objeto"),
            "posicion": match.span("objeto")
        }
        lista.append(diccionario)
    return lista


# CONSULTA 6
def consulta_6(texto, patron):
    regex = re.compile(patron)
    lista = []
    for match in regex.finditer(texto):
        diccionario = {
            "contenido": match.group("completo"),
            "posicion": match.span("referencia")
        }
        lista.append(diccionario)
    return lista
