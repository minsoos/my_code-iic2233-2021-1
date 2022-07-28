"""
Modulo contiene implementación principal del cliente
"""
import json
import threading
import socket
from interfaz import Controlador


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

    def __init__(self, host, port, log_activado=True):
        self.host = host
        self.port = port
        self.log_activado = log_activado

        # Inicializar UI
        self.controlador = Controlador(self)

        # Crear socket IPv4, TCP
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.iniciar_cliente()

    def iniciar_cliente(self):
        # Completar
        # IMPORTANTE: Si la conexión es exitosa, además de hacer lo que indica 
        # en el enunciado, debes invocar al método mostrar_login de self.controlador
        # self.controlador.mostrar_login()
        try:
            self.socket_cliente.connect((self.host, self.port))
        except ConnectionError:
            self.log(f"No se pudo conectar a {self.host}:{self.port}")
            self.socket_cliente.close()

        else:
            self.conectado = True
            thread_x = threading.Thread(target=self.escuchar_servidor, daemon=True)
            thread_x.start()
            print("llegué aquí")
            self.controlador.mostrar_login()

    def escuchar_servidor(self):
        """Ciclo principal que escucha al servidor.

        Recibe mensajes desde el servidor, y genera una respuesta adecuada.
        """
        while self.conectado:
            try:
                mensaje = self.recibir()
            except ConnectionResetError:
                self.log("Error de conexión con el servidor")
            else:
                print("manejaré el mensaje")
                retorno = self.controlador.manejar_mensaje(mensaje)
                print(f"manejar mensaje retorna {retorno}")

    def enviar(self, mensaje):
        """Envía un mensaje a un cliente.

        Argumentos:
            mensaje (dict): Contiene la información a enviar.
        """
        try:
            mensaje = self.codificar_mensaje(mensaje)
            largo_mensaje = len(mensaje).to_bytes(5, byteorder="little")
            self.socket_cliente.sendall(largo_mensaje + mensaje)
        except ConnectionError:
            self.socket_cliente.close()

    def recibir(self):
        """Recibe un mensaje del servidor.

        Recibe el mensaje, lo decodifica usando el protocolo establecido,
        y lo des-serializa (via decodificar_mensaje).

        Retorna:
            dict: contiene el mensaje, después de ser decodificado.
        """
        largo = self.socket_cliente.recv(5)
        largo = int.from_bytes(largo, byteorder="little")
        mensaje = bytearray()
        while len(mensaje) < largo:
            contenido_i = self.socket_cliente.recv(min(64, largo - len(mensaje)))
            mensaje += contenido_i
        return self.decodificar_mensaje(mensaje)

    def log(self, mensaje_consola):
        """Imprime un mensaje a la consola, sólo si la funcionalidad está activada.

        Argumentos:
            mensaje_consola (str): mensaje a imprimir.
        """
        if self.log_activado:
            print(mensaje_consola)

    def codificar_mensaje(self, mensaje):
        """Codifica y serializa un mensaje usando JSON.

        Argumentos:
            mensaje (dict): Contiene llaves de strings, con información útil a enviar a cliente.
              Los valores del diccionario deben ser serializables.

        Retorna:
            bytes: El mensaje serializado
        """
        try:
            # Create JSON object
            json_mensaje = json.dumps(mensaje)
            # Encode JSON object
            bytes_mensaje = json_mensaje.encode()

            return bytes_mensaje
        except json.JSONDecodeError:
            self.log("No se pudo codificar el mensaje")
            return b""

    def decodificar_mensaje(self, bytes_mensaje):
        """Decodifica y des-serializa bytes usando JSON.

        Argumentos:
            bytes_mensaje (bytes): Representa el mensaje serializado. Debe ser des-serializable
                y decodificable.

        Retorna:
            dict: El mensaje des-serializado, en su forma original.
        """
        try:
            mensaje = json.loads(bytes_mensaje)
            return mensaje
        except json.JSONDecodeError:
            self.log("No se pudo decodificar el mensaje")
            return dict()
