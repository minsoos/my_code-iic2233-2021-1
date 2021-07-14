"""
Modulo contiene implementación principal del servidor
"""
import json
import socket
import threading
from codificacion import decodificar_imagen, decodificar_mensaje, codificar_mensaje, codificar_imagen
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

    def __init__(self, host, port):
        self.host = host
        self.port = port

        # Crear atributo para el socket del servidor, pero vacío
        self.socket_servidor = None

        print("Inicializando servidor...")
        self.iniciar_servidor()

        # Crear diccionario de clientes de la forma { id : socket }
        self.clientes_conectados = dict()

        self.logica = Logica()

        # Crea y comienza thread encargado de aceptar clientes
        thread = threading.Thread(target=self.aceptar_clientes, daemon=True)
        self.conexiones()
        thread.start()
    
    def conexiones(self):
        self.logica.senal_enviar_mensaje.connect(self.enviar_mensaje)
        self.logica.senal_eliminar_cliente.connect(self.eliminar_cliente)
        self.logica.senal_enviar_imagen.connect(self.enviar_imagen)

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
            print(f"Un nuevo cliente con dirección {direccion_ip} ha sido aceptado")
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
                if mensaje is not None:
                    self.logica.caracterizar_mensaje(id_cliente, mensaje)

            except ConnectionResetError as error:
                print(f"ERROR: conexión con cliente {id_cliente} fue reseteada")
                self.eliminar_cliente(id_cliente)


    def enviar_mensaje(self, id_usuario, mensaje):
        """Envía un mensaje a un cliente.

        Argumentos:
            mensaje (dict): Contiene la información a enviar.
        """
        try:
            socket_cliente = self.clientes_conectados[id_usuario]
            mensaje = codificar_mensaje(mensaje)
            socket_cliente.sendall(mensaje)
        except (ConnectionError, KeyError):
            print("Hubo un error al enviar el mensaje")
            socket_cliente.close()
    
    def enviar_imagen(self, id_usuario, path_imagen):
        """Envía un mensaje a un cliente.

        Argumentos:
            mensaje (dict): Contiene la información a enviar.
        """
        try:
            socket_cliente = self.clientes_conectados[id_usuario]  
            imagen_en_bytes = codificar_imagen(path_imagen)
            socket_cliente.sendall(imagen_en_bytes)
        except (ConnectionError, KeyError):
            print("Hubo un error al enviar el mensaje")
            socket_cliente.close()

    def recibir(self, socket_cliente):
        """Recibe un mensaje del servidor.

        Recibe el mensaje, lo decodifica usando el protocolo establecido,
        y lo des-serializa (via decodificar_mensaje).

        Retorna:
            dict: contiene el mensaje, después de ser decodificado.
        """
        array = bytearray()

        largo = socket_cliente.recv(4)
        array += largo
        largo = int.from_bytes(largo, byteorder="big")

        tipo_mensaje = socket_cliente.recv(4)
        array += tipo_mensaje
        tipo_mensaje = int.from_bytes(tipo_mensaje, byteorder="little")

        if tipo_mensaje == 1:
            largo_chunk = 100
            color = socket_cliente.recv(4)
            array += color
        elif tipo_mensaje == 2:
            largo_chunk = 60
        else:
            raise ValueError("Error en recibir de cliente.py")

        parte_incontable = len(array)

        while len(array) - parte_incontable < largo:
            cabeza = socket_cliente.recv(4)
            parte_incontable += 4
            contenido_i = socket_cliente.recv(largo_chunk)
            array += cabeza + contenido_i

        if tipo_mensaje == 1:
            return decodificar_imagen(array)
        elif tipo_mensaje == 2:
            return decodificar_mensaje(array)
        else:
            raise ValueError("Error en recibir de cliente.py")

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente de clientes_conectados.

        Argumentos:
            id_cliente (int): la id del cliente a eliminar del diccionario.
        """
        with self.clientes_conectados_lock:
            print(f"Borrando socket del cliente {id_cliente}.")
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
        print("Desconectando clientes...")
        for id_cliente in list(self.clientes_conectados.keys()):
            self.eliminar_cliente(id_cliente)
        print("Cerrando socket de recepción...")
        self.socket_servidor.close()
        print("Guardando variables en memoria...")
        self.logica.guardar_variables()
