"""
Modulo contiene implementación principal del servidor
"""
import json
import socket
import threading
from logica import Logica


class Servidor:
    """
    Clase Servidor: Administra la conexión y la comunicación con los clientes

    Atributos:
        host: string que representa la dirección del host (como una URL o una IP address).
        port: int que representa el número de puerto en el cual el servidor recibirá conexiones.
        log_activado: booleano, controla si el programa "printea" en la consola (ver método log).
        socket_servidor: socket del servidor, encargado de recibir conexiones.
        clientes_conectados: diccionario que mantiene los sockets de los clientes actualmente
            conectados, de la forma { id : socket_cliente }.
        logica: instancia de Logica que maneja el funcionamiento interno del programa
    """

    _id_cliente = 0
    # Administra el acceso a clientes_conectados para evitar que se produzcan errores.
    clientes_conectados_lock = threading.Lock()

    def __init__(self, host, port, log_activado=True):
        self.host = host
        self.port = port
        self.log_activado = log_activado

        # Crear atributo para el socket del servidor, pero vacío
        self.socket_servidor = None

        self.log("Inicializando servidor...")
        self.iniciar_servidor()

        # Crear diccionario de clientes de la forma { id : socket }
        self.clientes_conectados = dict()

        self.logica = Logica(log_activado)

        # Crea y comienza thread encargado de aceptar clientes
        thread = threading.Thread(target=self.aceptar_clientes, daemon=True)
        thread.start()

    def iniciar_servidor(self):
        mi_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mi_sock.bind((self.host, self.port))
        mi_sock.listen()
        self.socket_servidor = mi_sock

    def aceptar_clientes(self):
        """Ciclo principal que acepta clientes.
        """
        while True:
            socket_cliente, direccion_ip = self.socket_servidor.accept()
            self.log(f"Un nuevo cliente con dirección {direccion_ip} ha sido aceptado")
            self.clientes_conectados_lock.acquire()
            self.clientes_conectados[self._id_cliente] = socket_cliente
            self.clientes_conectados_lock.release()
            escuchador = threading.Thread(target=self.escuchar_cliente, daemon=True,\
                args=(self._id_cliente, ))
            self._id_cliente += 1
            escuchador.start()

    def escuchar_cliente(self, id_cliente):
        """Ciclo principal que escucha a un cliente.

        Recibe mensajes de un cliente, y genera una respuesta adecuada o levanta
        una acción según el mensaje recibido.

        Argumentos:
            id_cliente (int): La id del cliente a escuchar.
        """
        while True:
            try:
                cliente = self.clientes_conectados[id_cliente]
                mensaje = self.recibir(cliente)
                
                
                respuesta, destinatarios = self.logica.manejar_mensaje(mensaje, id_cliente)
                for destinatario in destinatarios:
                    self.enviar(respuesta, self.clientes_conectados[destinatario])

            except ConnectionResetError as error:
                self.log(f"ERROR: conexión con cliente {id_cliente} fue reseteada")
                self.eliminar_cliente(id_cliente)


    def enviar(self, mensaje, socket_cliente):
        """Envía un mensaje a un cliente.

        Argumentos:
            mensaje (dict): Contiene la información a enviar.
            socket_cliente (socket): El socket objetivo al cual enviar el mensaje.
        """
        mensaje = self.codificar_mensaje(mensaje)
        largo_mensaje = len(mensaje)
        largo_mensaje_en_bytes = largo_mensaje.to_bytes(5, byteorder="little")

        socket_cliente.sendall(largo_mensaje_en_bytes + mensaje)

    def recibir(self, socket_cliente):
        """Recibe un mensaje del cliente.

        Recibe el mensaje, lo decodifica usando el protocolo establecido,
        y lo des-serializa (via decodificar_mensaje).

        Argumentos:
            socket_cliente (socket): El socket del cliente del cual recibir.

        Retorna:
            dict: contiene el mensaje, después de ser decodificado.
        """
        head = socket_cliente.recv(5)
        largo_mensaje = int.from_bytes(head, byteorder="little")
        mensaje = bytearray()
        while len(mensaje) < largo_mensaje:
            contenido_i = socket_cliente.recv(min(64, largo_mensaje - len(mensaje)))
            mensaje += contenido_i

        return self.decodificar_mensaje(mensaje)

    def log(self, mensaje_consola):
        """Imprime un mensaje a la consola, sólo si la funcionalidad está activada.

        Argumentos:
            mensaje_consola (str): mensaje a imprimir.
        """
        if self.log_activado:
            print(mensaje_consola)

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente de clientes_conectados.

        Argumentos:
            id_cliente (int): la id del cliente a eliminar del diccionario.
        """
        with self.clientes_conectados_lock:
            self.log(f"Borrando socket del cliente {id_cliente}.")
            # Obtener socket
            socket_cliente = self.clientes_conectados[id_cliente]
            # Cerrar socket
            socket_cliente.close()
            # Borrar entrada del diccionario
            del self.clientes_conectados[id_cliente]
            # Borrar usuario de los usuarios activos (Logica)
            self.logica.desconectar_usuario(id_cliente)

    def cerrar_servidor(self):
        """
        Ejecuta las acciones necesarias para cerrar el servidor:
         - Desconecta los clientes
         - Cierra su socket
         - Persiste variables en memoria
        """
        self.log("Desconectando clientes...")
        for id_cliente in list(self.clientes_conectados.keys()):
            self.eliminar_cliente(id_cliente)
        self.log("Cerrando socket de recepción...")
        self.socket_servidor.close()
        self.log("Guardando variables en memoria...")
        self.logica.guardar_variables()

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
            self.log("ERROR: No se pudo codificar el mensaje")
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
            self.log("ERROR: No se pudo decodificar el mensaje")
            return dict()
