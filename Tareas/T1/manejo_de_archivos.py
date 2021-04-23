def lista_canales(ruta = "canales.csv"):
    with open(ruta, encoding="UTF-8") as archivo:
        lineas = archivo.readlines()
        if lineas[0] != "nombre,tamaño,dificultad\n":
            return "no abriste una lista de canales"
    lista_canales = []
    for linea in lineas:
        linea.strip().split(",")
        canal_aux = Canal(linea[0], linea[1], linea[2])
        lista_canales.append(canal_aux)
    return lista_canales
        