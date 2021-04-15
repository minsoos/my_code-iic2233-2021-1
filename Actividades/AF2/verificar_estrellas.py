from cargar_datos import cargar_estrellas, cargar_nombres_estrellas_cercanas


def verificar_alias_estrella(estrella):
    alias = estrella.alias
    letras_alias = alias[0:2]
    numeros_alias = alias[2:4]
    bool1 = numeros_alias.isdigit()
    bool2 = letras_alias.isupper()
    bool3 = "F" not in letras_alias
    if not bool1 or not bool2 or not bool3:
        raise ValueError("Error: El alias de la estrella es incorrecto.", bool1, bool2, bool3)


def corregir_alias_estrella(estrella):
    try:
        verificar_alias_estrella(estrella)
    except ValueError as err:
        print(err.args[0])
        alias = estrella.alias
        letras_alias = alias[0:2]
        numeros_alias = alias[2:4]
        if err.args[3] == False:
            alias = alias.replace("F", "T")
        if err.args[1] == False:
            #Acá suponemos que están cambiados
            alias = numeros_alias + letras_alias
        estrella.alias = alias
        print(f"El alias de {estrella.nombre} fue correctamente corregido.\n")


def verificar_distancia_estrella(estrella):
    if estrella.distancia < 0:
        raise ValueError("Error: Distancia negativa.")


def corregir_distancia_estrella(estrella):
    try:
        verificar_distancia_estrella(estrella)
    except ValueError as err:
        print(err)
        estrella.distancia = -estrella.distancia
        print(f"La distancia de la estrella {estrella.nombre} fue corregida.\n")

def verificar_magnitud_estrella(estrella):
    if not isinstance(estrella.magnitud, float):
        raise TypeError("Error: Magnitud no es del tipo correcto.")

def corregir_magnitud_estrella(estrella):
    try:
        verificar_magnitud_estrella(estrella)
    except TypeError as err:
        print(err)
        magnitud = estrella.magnitud
        magnitud = magnitud.replace(";",".")
        try:
            estrella.magnitud = float(magnitud)
            
        except ValueError:
            pass
        else:
            print(f"La magnitud de la estrella {estrella.nombre} fue corregida.\n")

        


def dar_alerta_estrella_cercana(nombre_estrella, diccionario_estrellas):
    try:
        estrellita = diccionario_estrellas[nombre_estrella]
        print(f"Estrella {nombre_estrella} está en nuestra base de datos.")
        print(f"Su alias es {estrellita.alias}.")
    except KeyError:
        print(f"Estrella {nombre_estrella} NO está en nuestra base de datos.")
        print("¡Alerta, puede ser una trampa de algún extraterrestre!")



if __name__ == "__main__":
    diccionario_estrellas = cargar_estrellas("estrellas.csv")
    nombres_estrellas = cargar_nombres_estrellas_cercanas("estrellas_cercanas.txt")

    # Descomenta las funciones que quieras probar de la actividad
    print("Revisando posibles errores en las estrellas...\n")
    for estrella in diccionario_estrellas.values():
        corregir_alias_estrella(estrella)
        corregir_distancia_estrella(estrella)
        corregir_magnitud_estrella(estrella)
        pass

    print("Revisando estrellas inexistentes...\n")
    for nombre_estrella in nombres_estrellas:
        dar_alerta_estrella_cercana(nombre_estrella, diccionario_estrellas)
        pass
