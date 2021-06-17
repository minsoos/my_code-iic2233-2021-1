"""
Este módulo contiene funciones para el manejo general de los bytes de las
imágenes

Corresponde a la parte de Bytes
"""


def tuplas_desde_bytes(bytes_):
    """
    Recibe un bytearray proveniente de una imagen, que representa la información
    condensada de cada pixel. Se deben separar los pixeles (un pixel son 4 bytes
    en el bytearray) en una lista de tuplas.

    Argumentos:
        bytes_ (bytearray): La información a separar en tuplas.

    Retorna:
        list[tuple[int]]: lista de tuplas separadas
    """
    lista_final = []
    for i in range(0, len(bytes_), 4):
        pixel = bytes_[i:i+4]
        lista_i = []
        for byte in pixel:
            lista_i.append(byte)
        lista_final.append(tuple(lista_i))
        
    return lista_final


def bytes_desde_tuplas(tuplas):
    """
    Recibe una lista de tuplas, y las transforma en un bytearray. Realiza la
    función inversa de tuples_from_bytes.

    Argumentos:
        tuplas (list[tuple[int]]): Lista de tuplas a juntar

    Retorna:
        bytearray: bytes resultantes de juntar las información de las tuplas
    """
    bytearray_final = bytearray()
    
    for tupla in (tuplas):
        bytearray_i = bytearray()
        for entero in tupla:
            bytearray_i.append(entero)

        bytearray_final.extend(bytearray_i)
    
    return bytearray_final


def recuperar_contenido(bytearray_):
    """
    Recibe una ruta referente al archivo corrompido, tu tienes que sobreescrivir ese mismo archivo
    despues de corrigirlo con el algoritimo mencionado en el Enunciado.
    """
    contenido = bytearray_
    bytearray_final = bytearray()

    impar = True
    for byte_i in range(0, len(contenido), 2):
        primer_byte = contenido[byte_i]
        segundo_byte = contenido[byte_i + 1]
        if impar:
            if primer_byte == 0:
                byte = segundo_byte * 2
            elif primer_byte == 1:
                byte = segundo_byte * 2 +1
            else:
                raise ValueError("error en contenido")
        else:
            if segundo_byte == 0:
                byte = primer_byte * 2
            elif segundo_byte == 1:
                byte = primer_byte * 2 +1
            else:
                raise ValueError("error en contenido")
        
        bytearray_final += bytes(byte)

        impar = not impar



    # for pos_i, byte_i in enumerate(contenido):

    #     if pos_i % 2 == 1:
    #         bytearray_final.append(byte_1)
    #         bytearray_final.append(byte_2)
    #     elif pos_i % 2 == 0:
    #         bytearray_final.append(byte_2)
    #         bytearray_final.append(byte_1)
    #     else:
    #         raise ValueError("error en recuperar_contenido")

    return bytearray_final
    
    


def organizar_bmp(info_bytes):
    """
    Separa la información de la imagen en formato bmp en sus componentes
    principales

    Argumentos:
        info_bytes (bytearray): bytes representando la info de la imagen bmp

    Retorna:
        tuple[bytearray]: contiene el header, DIB Header, los pixeles, y el EOF
    """
    # No debes modificar esta función
    header = info_bytes[:15]
    dib_header = info_bytes[15:125]
    pixel_data = info_bytes[125:-1]
    eof = [info_bytes[-1]]
    return header, dib_header, pixel_data, eof


def int_desde_bytes(bytes_):
    """
    Decodifica el valor de un bytearray a un int con codificación little endian

    Argumentos:
        bytes_ (bytearray): Los bytes a decodificar

    Retorna:
        int: valor numérico correspondiente a los bytes
    """
    # No debes modificar esta función
    return int.from_bytes(bytes_, byteorder="little")


if __name__ == "__main__":
    """
    PUEDES PROBAR TU CÓDIGO AQUÍ
    """
