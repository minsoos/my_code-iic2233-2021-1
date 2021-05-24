class VentanaPostRonda(QWindow):
    def __init__(self) -> None:
        super().__init__()
        '''
        Esta ventana contendrá la información del juego que acaba
        de ocurrir, podrá elegir salir a la ventana de inicio o
        continuar jugando, e ir a la ventana de preparación
        '''
        #label de fondo
        #Label de título
        #label de puntaje
        #label de cantidad de items malos
        #label de cantidad de items buenos
        #Label de notificación de juego
        #QPushButton de continuar partida
        #QPushButton de salir


class LogicaVentanaPostRonda():
    def __init__(self) -> None:
        '''
        Este es el backend de la ventana post ronda
        '''
    def cargar_ventana(self):
        '''
        Envía una señal para cargar la ventana con sus labels
        '''

    def salir_a_inicio(self):
        '''
        Te lleva a la ventana de inicio y cierra la actual
        '''

    def continuar_juego(self):
        '''
        Te lleva a la ventana de preparación y cierra la actual
        '''