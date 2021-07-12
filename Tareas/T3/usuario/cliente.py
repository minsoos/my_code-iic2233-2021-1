"""
Modulo contiene implementación principal del cliente
"""
import json
import threading
import socket
from codificacion import decodificar_imagen, decodificar_mensaje, codificar_mensaje
from controlador import Controlador
from utils import cargar_parametros, normalizar_ruta


class Cliente:
    """
    Clase Cliente: Administra la conexión y la comunicación con el servidor.

    Atributos:
        host: string que representa la dirección del host (como una URL o una IP address).
        port: int que representa el número de puerto al cual conectarse.
        log_activado: booleano, controla si el programa "printea" en la consola (ver método log).
        controlador: instancia de Controlador, maneja la interfaz gráfica del programa.
        conectado: booleano, indica si el cliente se encuentra conectado al servidor.
        socket_cliente: socket del cliente, conectado al servidor.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port


        # Inicializar UI
        
        parametros = cargar_parametros()
        dict_parametros = dict()
        logo = parametros["RUTAS"]["IMAGEN_DRON"]
        dict_parametros["ruta_logo"] = logo
        nubes = parametros["RUTAS"]["IMAGEN_NUBES"]
        dict_parametros["ruta_nubes"] = nubes
        for elemento in dict_parametros:
            dict_parametros[elemento] = normalizar_ruta(dict_parametros[elemento])
        self.controlador = Controlador(**dict_parametros)


        self.diccionario_colores = {
            1: "Azul",
            2: "Rojo",
            3: "Verde",
            4: "Amarillo"
        }

        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.iniciar_cliente()
        self.conexiones()
    
    def conexiones(self):
        self.controlador.senal_enviar_mensaje.connect(self.enviar)

    def iniciar_cliente(self):
        try:
            self.socket_cliente.connect((self.host, self.port))
        except ConnectionError:
            print(f"No se pudo conectar a {self.host}:{self.port}")
            self.socket_cliente.close()

        else:
            self.conectado = True
            thread_x = threading.Thread(target=self.escuchar_servidor, daemon=True)
            thread_x.start()

    def escuchar_servidor(self):
        """Ciclo principal que escucha al servidor.

        Recibe mensajes desde el servidor, y genera una respuesta adecuada.
        """
        while self.conectado:
            try:
                mensaje = self.recibir()
            except ConnectionResetError:
                print("Error de conexión con el servidor")
                self.socket_cliente.close()
            else:
                retorno = self.controlador.manejar_mensaje(mensaje)

    def enviar(self, mensaje):
        """Envía un mensaje a un cliente.

        Argumentos:
            mensaje (dict): Contiene la información a enviar.
        """

        try:
            mensaje = codificar_mensaje(mensaje)
            self.socket_cliente.sendall(mensaje)
        except ConnectionError:
            self.socket_cliente.close()
        
        # while len(array) - parte_incontable < largo:
        #     if largo - (len(mensaje) - parte_incontable) >= largo_chunk:
        #         cabeza = self.socket_cliente.recv(4)
        #         contenido_i = self.socket_cliente.recv(largo_chunk)
        #         relleno = b""
        #     else:
        #         faltante = largo - (len(array) - parte_incontable)
        #         cabeza = self.socket_cliente.recv(4)
        #         contenido_i = self.socket_cliente.recv(faltante)
        #         relleno = b'\x 00' * (largo_chunk - faltante)
        #     array += cabeza + contenido_i + relleno

    def recibir(self):
        """Recibe un mensaje del servidor.

        Recibe el mensaje, lo decodifica usando el protocolo establecido,
        y lo des-serializa (via decodificar_mensaje).

        Retorna:
            dict: contiene el mensaje, después de ser decodificado.
        """
        array = bytearray()
        try:
            largo = self.socket_cliente.recv(4)
        except ConnectionError:
            print("Error al escuchar al servidor")
        array += largo
        largo = int.from_bytes(largo, byteorder="big")

        tipo_mensaje = self.socket_cliente.recv(4)
        array += tipo_mensaje
        tipo_mensaje = int.from_bytes(tipo_mensaje, byteorder="little")

        if tipo_mensaje == 1:
            largo_chunk = 100
            color = self.socket_cliente.recv(4)
            array += color
        elif tipo_mensaje == 2:
            largo_chunk = 60
        else:
            raise ValueError("Error en recibir de cliente.py")

        parte_incontable = len(array)

        while len(array) - parte_incontable < largo:
            cabeza = self.socket_cliente.recv(4)
            parte_incontable += 4
            contenido_i = self.socket_cliente.recv(largo_chunk)
            array += cabeza + contenido_i

        if tipo_mensaje == 1:
            return decodificar_imagen(array)
        elif tipo_mensaje == 2:
            return decodificar_mensaje(array)
        else:
            raise ValueError("Error en recibir de cliente.py")
