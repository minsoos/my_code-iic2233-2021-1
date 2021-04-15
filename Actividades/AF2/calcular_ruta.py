from excepciones_estrellas import RutaPeligrosa


# No modificar esta función
def verificar_condiciones_estrella(estrella):
    if estrella.luminosidad > 15500:
        raise RutaPeligrosa("luz", estrella.nombre)
    elif estrella.magnitud > 4:
        raise RutaPeligrosa("tamaño", estrella.nombre)
    elif estrella.temperatura > 7200:
        raise RutaPeligrosa("calor", estrella.nombre)


# Completar
def generar_ruta_estrellas(estrellas):
    lista_ruta = list()
    for estrella in estrellas:
        try:
            es_segura = verificar_condiciones_estrella(estrella)
        except RutaPeligrosa as peligro:
            print(peligro)
        else:
            lista_ruta.append(estrella)
            print(f'¡La estrella {estrella.nombre} se ha agregado a tu ruta!' + u'\x02' + '\n')
    return lista_ruta
