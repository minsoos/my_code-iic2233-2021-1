class VentanaJuego(QWindow):
    def __init__(self) -> None:
        super().__init__()
        #Label vida jugador
        #Label número de ronda
        #Label tiempo restante para finalizar ronda
        #Label ítems buenos atrapados
        #Label ítems malos atrapados
        #Label puntaje actual
        #QPushButton pausar el juego
        #QpushButton salir de juego
        #Label fondo
        #Labels de objetos
    
    def cargar_datos(self,):
        '''
        A este método lo llama una señal del backend,
        y carga los datos que esta le entrega a los labels
        '''
    def actualizar_tablero(self):
        '''
        este método actualiza los labels de 
        la partida cuando se llama
        '''

    def actualizar_personaje(self):
        '''
        este método actualiza los labels de 
        personaje cuando se llama
        '''
    
class LogicaVentanaJuego():

    senal_enviar_actualizacion_tablero = pyqtSignal()
    senal_cargar_tablero = pyqtSignal()
    senal_cambiar_boton_pausa = pyqtSignal()

    def __init__(self) -> None:
        '''
        Este es el backend de la ventana juego, y se encarga de
        realizar los procesos de esta
        '''

    def cargar_juego(self):
        '''
        Este método se encargará de leer el progreso de la partida
        cuando es llamado, y enviar la información al frontend 
        mediante la señal senal_enviar_actualizacion_tablero
        Además carga los objetos
        '''

    def tecla_presionada(self, teclas):
        '''
        Este método se encarga de analizar teclas presionadas y
        reenviarlos a sus respectivos métodos
        '''

    def enviar_actualizacion_tablero(self):
        '''
        Este método se encargará de leer el progreso de la partida
        cuando es llamado y enviar la información al frontend 
        mediante la señal senal_enviar_actualizacion_tablero.
        A diferencia de cargar tablero, este sólo cambia lo que varía
        dentro del juego
        '''

    def pausa_juego(self):
        '''
        Este método se encarga de, cuando es llamado,
        reanudar el juego si está pausado y pausarlo si no 
        mediante la señal senal_enviar_actualizacion_tablero.
        Además cambia el botón de pausa
        '''

    def salir_juego(self):
        '''
        Este método se encarga de, cuando es llamado,
        salir del juego y llevar a la ventana post ronda
        '''

    def cheats(self, teclas):
        '''
        Comprueba si se ejecutó algún cheat, y los ejecuta
        '''