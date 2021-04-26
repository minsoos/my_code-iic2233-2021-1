from parametros import RUTA_CANALES, RUTA_BARCOS, RUTA_MERCANCIA, RUTA_TRIPULANTES
import menus
from canales import Canal
from barcos import BarcoPasajeros, BarcoCarguero, Buque
from mercancia import Mercancia
from tripulacion import DCCapitan, DCCocinero, DCCarguero


def dict_canales():
    with open(RUTA_CANALES, encoding="UTF-8") as archivo:
        lineas = archivo.readlines()
        if lineas[0] != "nombre,tamaño,dificultad\n":
            print("no abriste una lista de canales")
            print("Arregla tus paths en parametros.py para correr el programa")
            menus.menu_de_inicio()
        else:
            dict_canales = {}
            for linea in range(1, len(lineas)):
                linea_aux = lineas[linea].strip().split(",")
                canal_aux = Canal(linea_aux[0], int(linea_aux[1]), linea_aux[2])
                dict_canales[linea_aux[0]] = canal_aux
            return dict_canales


def dict_mercancia():
    with open(RUTA_MERCANCIA, encoding="UTF-8") as archivo:
        lineas = archivo.readlines()
        if lineas[0] != "lote,tipo,tiempo de expiración,peso\n":
            print("no abriste una lista de mercancia")
            print("Arregla tus paths en parametros.py para correr el programa")
            menus.menu_de_inicio()
        else:
            dict_mercancia = {}
            for linea in range(1, len(lineas)):
                linea_aux = lineas[linea].strip().split(",")
                l = linea_aux
                mercancia_aux = Mercancia(int(l[0]), l[1], int(l[2]), int(l[3])/4)
                dict_mercancia[int(linea_aux[0])] = mercancia_aux
            return dict_mercancia


def dict_tripulantes():
    with open(RUTA_TRIPULANTES, encoding="UTF-8") as archivo:
        lineas = archivo.readlines()
        if lineas[0] != "nombre,tipo,años de experiencia\n":
            print("no abriste una lista de mercancia")
            print("Arregla tus paths en parametros.py para correr el programa")
            menus.menu_de_inicio()
        else:
            dict_tripulantes = {}
            for linea in range(1, len(lineas)):
                linea_aux = lineas[linea].strip().split(",")
                tipo = linea_aux[1]
                if tipo == "DCCapitán":
                    clase = DCCapitan
                if tipo == "DCCocinero":
                    clase = DCCocinero
                if tipo == "DCCarguero":
                    clase = DCCarguero
                tripulante_aux = clase(linea_aux[0], int(linea_aux[2]))
                dict_tripulantes[linea_aux[0]] = tripulante_aux
            return dict_tripulantes


def dict_barcos():
    with open(RUTA_BARCOS, encoding="UTF-8") as archivo:
        lineas = archivo.readlines()
        if not lineas[0].endswith("origen,tripulación,carga\n"):
            print("no abriste una lista de barcos")
            print("Arregla tus paths en parametros.py para correr el programa")
            menus.menu_de_inicio()
        else:
            dict_barcos = {}
            for linea in range(1, len(lineas)):
                linea_aux = lineas[linea].strip().split(",")
                # Metemos en un dict los argumentos
                # Algunos debemos sacarlos desde funciones aparte
                dict_de_kwargs = {"nombre": linea_aux[0]}
                dict_de_kwargs["costo_mantencion"] = float(linea_aux[2])
                dict_de_kwargs["velocidad_base"] = int(linea_aux[3])
                dict_de_kwargs["pasajeros"] = int(linea_aux[4])
                dict_de_kwargs["carga_maxima"] = int(linea_aux[5])
                dict_de_kwargs["moneda_origen"] = linea_aux[6]
                # La siguiente parte de código es para instanciar a la tripulación
                tripulacion = linea_aux[7].split(";")
                dict_tripulantes_aux = dict_tripulantes()
                tripulacion_definitiva = []
                for tripulante in tripulacion:
                    if tripulante in dict_tripulantes_aux.keys():
                        tripulacion_definitiva.append(dict_tripulantes_aux[tripulante])
                dict_de_kwargs["tripulacion"] = tripulacion_definitiva
                # Aquí termina el bloque de tripulación#######
                # La siguiente parte de código es para instanciar a la mercancia
                mercancia = linea_aux[8].split(";")
                dict_mercancia_aux = dict_mercancia()
                mercancia_definitiva = []
                for mercancia_n in mercancia:
                    mercancia_n = int(mercancia_n)
                    if mercancia_n in dict_mercancia_aux.keys():
                        mercancia_definitiva.append(dict_mercancia_aux[mercancia_n])
                dict_de_kwargs["mercancia"] = mercancia_definitiva
                # Aquí termina el bloque de mercancia#######
                # Terminamos de llenar el kwargs para barco
                # Ahora según el tipo de barco, instanciamos cada clase
                tipo_barco = linea_aux[1]
                if tipo_barco == "Pasajero":
                    sub_clase_barco = BarcoPasajeros
                elif tipo_barco == "Carguero":
                    sub_clase_barco = BarcoCarguero
                elif tipo_barco == "Buque":
                    sub_clase_barco = Buque
                # Sabemos el tipo de barco, ahora lo instanciamos
                barco_aux = sub_clase_barco(dict_de_kwargs)
                if 1 <= len(barco_aux.tripulacion) <= 3:
                    dict_barcos[linea_aux[0]] = barco_aux
            return dict_barcos


##  DCCapitan, DCCocinero, DCCarguero
if __name__ == "__main__":
    dict_barcos = dict_barcos()
    mi_barco = dict_barcos["La Nao Victoria"]
    print(mi_barco.pasajeros)
    print(mi_barco.mercancia)