class RutaPeligrosa(Exception):
    def __init__(self, tipo_peligro, nombre_estrella):
        self.tipo_peligro = tipo_peligro
        self.nombre_estrella = nombre_estrella
        print('¡Alto ahí viajero! Hay una amenaza en tu ruta...')


    def dar_alerta_peligro(self):
        peligro = self.tipo_peligro
        if peligro == "luz":
            print("¡Ten cuidado, que con tanta luz no podrás ver :(!")
        elif peligro == "tamaño":
            print("¡Ooops! Esa estrella es demasiado grande...")
        elif peligro == "calor":
            print("¡Alerta! ¡Alerta! ¡Peligro inminente de quedar carbonizados!")
        print(f"La Estrella {self.nombre_estrella} ha quedado fuera de tu ruta.\n")
