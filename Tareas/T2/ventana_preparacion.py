class VentanaPreparacion(QWindow):
    def __init__(self) -> None:
        super().__init__()
        '''
        Front end de la ventana donde el jugador puede elegir
        su personaje (por defecto viene homero), además de su
        dificultad. Además puede ver cómo va el avance de su
        juego en curso, ver su vida, puntaje, items buenos y
        malos recogidos y rondas superadas.
        En este mismo, el jugador se puede mover a lo largo
        del mapa, donde cada personaje, si se desplaza hacia
        su tablero, entrará a la ventana de juego
        '''
        #QLabel logo
        #QSpinBox para dificultad
        #QLabel para número de ronda
        #Qlabel para puntaje
        #QLabel para ítems malos
        #QLabel para ítems buenos
        #QLabel para vida, intentando crear una barra
        #QPixmap con fondo de imagen de springfield
        #QLabel del personaje
        #QPushButton salir del juego
    def entrar_a_juego(self):
        '''
        Este método se llama cuando el personaje está en un
        lugar de juego. Si está en el que le corresponde, debe
        avanzar a la ventana de juego. De lo contrario, un label
        debe avisar que ese lugar no le corresponde
        '''


class LogicaVentanaPreparacion():
    def __init__(self) -> None:
        '''
        Backend de VentanaPreparacion. Aquí se cargan los
        valores de los parámetros correspondientes, además,
        maneja la entrada y salida de esta ventana
        '''
    def cargar_datos(self, partida):
        '''
        Recibe una instancia de la clase partida, y de
        acuerdo a sus atributos, carga la ventana con sus
        datos
        '''

    def cheat_aumentar_vida(self, teclas):
        '''
        Comprueba si se ejecutó el cheat de aumentar vida
        y lo ejecuta
        '''