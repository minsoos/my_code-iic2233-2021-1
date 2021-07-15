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

def ordenamiento_por_turno(objeto):
    return objeto["turno"]

def ordenamiento_por_puntaje(objeto):
    return objeto[1]