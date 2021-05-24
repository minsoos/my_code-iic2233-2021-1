
class ProgresoPartida():
    def __init__(self) -> None:
        '''
        Esta clase guarda el avance de una partida
        '''
        self.puntaje = 0
        self.items_buenos = 0
        self.items_malos = 0
        self.dificultad = None
        self.personaje = Homero()
        self.ronda = 1

    def iniciar_juego(self):
        '''
        Este método se encarga de iniciar un
        nuevo juego
        '''
    
    def acabar_partida(self):
        '''
        Este método se encarga de terminar la
        partida, llevándote a la ventana post-ronda
        '''


