from abc import ABC, abstractmethod
import random
from personas import Trabajador


# Completar
class Local(ABC):

    def __init__(self, productos, nombre, aforo, trabajador):
        # No modificar
        self.clientes = []
        self.productos = productos
        self.nombre = nombre
        self.aforo = aforo
        self.trabajador = trabajador

        self.abierto = not trabajador.contagiado
        self.__utilidades = 0
        self.clientes_rechazados = 0
        self.categoria = None

    @property
    def utilidades(self):
        return self.__utilidades
    
    @utilidades.setter
    def utilidades(self, cambio):
        if self.__utilidades + cambio >= 0:
            self.__utilidades += cambio
        else:
            self.__utilidades = 0
            self.abierto = False

    def cliente_ingresa(self, cliente):
        # No modificar
        if self.aforo <= len(self.clientes):
            print("Aforo lleno, vayase a casa")
            self.clientes_rechazados += 1
            return False

        if not cliente.contagiado:
            self.clientes.append(cliente)
            print("-" * 75)
            print(f"Hola {cliente.nombre} bienvenid@ a {self.nombre}")
            return True

        self.trabajador.generar_posible_contagio()
        print("-" * 75)
        print((
            f"{cliente.nombre} tiene Progravirus e intentó "
            f"ingresar a {self.nombre}, debe retirarse"
        ))

        if self.trabajador.contagiado:
            print(f"{self.trabajador.nombre} se ha contagiado por {cliente.nombre}")
            print(f"Se cierra el {self.nombre}")
            self.abierto = False

        self.clientes_rechazados += 1
        return False


    def obtener_producto_a_vender(self):
        # No modificar
        nombre_producto = random.choice(list(self.productos.keys()))
        return nombre_producto

    def entregar_resumen(self):
        # No modificar
        # Pagamos sueldo a trabajador
        self.utilidades -= self.trabajador.sueldo
        estado = "Abierto"

        if not self.abierto:
            estado = "Cerrado por utilidades"

        if self.trabajador.contagiado:
            estado = "Cerrado por Progravirus"
            self.abierto = False

        print("")
        print("")
        print(self.nombre.upper().center(50))
        print("")
        print(f"{'UTILIDADES:':45s}{str(self.utilidades)}")
        print(f"{'ESTADO:':45s}{estado}")
        print(f"{'NÚMERO DE CLIENTES:':45s}{str(len(self.clientes)) + '/' + str(self.aforo)}")
        print(f"{'CLIENTES RECHAZADOS:':45s}{self.clientes_rechazados}")


# Completar
class Entretenimiento(Local):

    def __init__(self, productos, nombre, aforo, trabajador):
        super().__init__(productos, nombre, aforo, trabajador)
        self.categoria = "Entretenimiento"
    def cliente_ingresa(self, cliente):
        entra = super().cliente_ingresa(cliente)
        if entra == True:
            self.sanitizar_juegos()
            return True
        else:
            return False
    def sanitizar_juegos(self):
        # No modificar
        print("Las instalaciones estan sanitizadas, A JUGAR!")


# Completar
class Comida(Local):

    def __init__(self, productos, nombre, aforo, trabajador):
        super().__init__(productos, nombre, aforo, trabajador)
        self.categoria = "Comida"

    def cliente_ingresa(self, cliente):
        entra = super().cliente_ingresa(cliente)
        if entra == True:
            self.entregar_menu()
            return True
        else:
            return False

    def entregar_menu(self):
        # No modificar
        print("Repartiendo menús")


# Completar
class Tienda(Local):

    def __init__(self, productos, nombre, aforo, trabajador):
        super().__init__(productos, nombre, aforo, trabajador)
        self.categoria = "Tienda"

    def cliente_ingresa(self, cliente):
        entra = super().cliente_ingresa(cliente)
        if entra == True:
            self.anunciar_oferta()
            return True
        else:
            return False

    def anunciar_oferta(self):
        # No modificar
        # Producto al azar que estara en oferta!
        producto_oferta = random.choice(list(self.productos.keys()))
        precio_oferta = self.productos[producto_oferta]
        print(f"Aproveche la de DCCofertas: {producto_oferta} a solo .. {precio_oferta}!!!!")


# Completar
class Casino(Entretenimiento, Comida):

    def __init__(self, productos, nombre, aforo, trabajador):
        super().__init__(productos, nombre, aforo, trabajador)
        self.categoria = "Casino"

    def cliente_ingresa(self, cliente):
        # No modificar
        if self.aforo <= len(self.clientes):
            print("Aforo lleno, vayase a casa")
            self.clientes_rechazados += 1
            return False

        if not cliente.contagiado and cliente.edad >= 18:
            self.clientes.append(cliente)
            print("-" * 75)
            print(f"Hola {cliente.nombre} bienvenid@ a {self.nombre}")
            self.sanitizar_juegos()
            self.entregar_menu()
            return True

        self.trabajador.generar_posible_contagio()
        print("-" * 75)
        print((
            f"{cliente.nombre} tiene Progravirus e intentó "
            f"ingresar a {self.nombre}, debe retirarse"
        ))
        self.clientes_rechazados += 1
        return False



# Completar
class Supermercado(Comida, Tienda):

    def __init__(self, productos, nombre, aforo, trabajador):
        super().__init__(productos, nombre, aforo, trabajador)
        self.categoria = "Supermercado"

    def cliente_ingresa(self, cliente):
        # No modificar
        if self.aforo <= len(self.clientes):
            print("Aforo lleno, vayase a casa")
            self.clientes_rechazados += 1
            return False

        if not cliente.contagiado:
            self.clientes.append(cliente)
            print("-" * 75)
            print(f"Hola {cliente.nombre} bienvenid@ a {self.nombre}")
            self.anunciar_oferta()
            self.entregar_menu()
            return True

        self.trabajador.generar_posible_contagio()
        print("-" * 75)
        print((
            f"{cliente.nombre} tiene Progravirus e intentó "
            f"ingresar a {self.nombre}, debe retirarse"
        ))
        self.clientes_rechazados += 1
        return False


if __name__ == "__main__":
    cruz = Trabajador("Cristian", 22, 0, 12000, "McGoofy's")
    mc = Comida({"hamburguesas": 2000, "bebida": 1000}, "McGoofy's", 5, cruz)
    mc.entregar_resumen()
