import json
"""
Modulo para funciones de codificacion y decodificacion para envio de mensajes.
Recuerda, no debes modificar los argumentos que recibe cada funcion,
y debes entregar exactamente lo que esta pide en el enunciado.
"""


# Codificar un mensaje a un bytearray segun el protocolo especificado.
def codificar_mensaje(mensaje):
    try:
        # Create JSON object
        mensaje = json.dumps(mensaje)
        mensaje = mensaje.encode(encoding="UTF-8")
    except json.JSONDecodeError:
        print("ERROR: No se pudo codificar el mensaje")
        return b""


    largo = len(mensaje)

    array = bytearray()
    array += largo.to_bytes(4, byteorder="big")
    tipo = 2
    array += tipo.to_bytes(4, byteorder="little")


    bytes_incontables = len(array)
    contador_chunks = 0
    posicion_cursor = 0

    while len(array) - bytes_incontables < largo:
        array += contador_chunks.to_bytes(4, byteorder="big")
        bytes_incontables += 4

        if posicion_cursor + 60 < largo:
            array += mensaje[posicion_cursor:posicion_cursor + 60]
            posicion_cursor += 60
            contador_chunks += 1
        else:
            array += mensaje[posicion_cursor:largo]
            relleno = b'\0' * (60 - (largo - posicion_cursor))
            array += relleno
    
    return array

# Decodificar un bytearray para obtener el mensaje original.
def decodificar_mensaje(mensaje):
    largo_bytes = len(mensaje) - 8
    largo = int.from_bytes(mensaje[:4], byteorder="big")
    cursor = 8
    array = bytearray()
    while len(array) < largo and largo_bytes > 0:
        cursor += 4
        largo_bytes -= 4
        if largo - len(array) > 60:
            array += mensaje[cursor:cursor + 60]
            cursor += 60
        else:
            array += mensaje[cursor:cursor + 60 - (largo_bytes - largo)]
    try:
        mensaje = array.decode(encoding="UTF-8")
        mensaje = json.loads(array)
        return mensaje
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("ERROR: No se pudo decodificar el mensaje")

# Codificar una imagen a un bytearray segun el protocolo especificado.
def codificar_imagen(ruta):
    mensaje = obtener_bytes_imagen(ruta)
    
    largo = len(mensaje)
    array = bytearray()
    array += largo.to_bytes(4, byteorder="big")
    array += (1).to_bytes(4, byteorder="little")
    array += int(ruta[-5]).to_bytes(4, byteorder="big")

    bytes_incontables = len(array)
    contador_chunks = 0
    posicion_cursor = 0

    while len(array) - bytes_incontables < largo:
        array += contador_chunks.to_bytes(4, byteorder="big")
        bytes_incontables += 4

        if posicion_cursor + 100 < largo:
            array += mensaje[posicion_cursor:posicion_cursor + 100]
            posicion_cursor += 100
            contador_chunks += 1
        else:
            array += mensaje[posicion_cursor:largo]
            relleno = b'\0' * (100 - (largo - posicion_cursor))
            array += relleno

    return array

def obtener_bytes_imagen(ruta):
    """
    Recibe un ruta de una imagen, y codifica sus bytes a un string utf-8
    """
    with open(ruta, "rb") as archivo_imagen:
        imagen_bytes = archivo_imagen.read()
        imagen_codificada = imagen_bytes # b64encode(imagen_bytes).decode(encoding='ASCII')
    return imagen_codificada

# Decodificar un bytearray a una lista segun el protocolo especificado.
def decodificar_imagen(mensaje):
    largo = int.from_bytes(mensaje[:4], byteorder="big")
    color = int.from_bytes(mensaje[4:8], byteorder="little")
    cursor = 8
    array = bytearray()
    while len(array) < largo:
        cursor += 4
        array += mensaje[cursor:cursor + 100]
        cursor += 100

    return [array, color]
