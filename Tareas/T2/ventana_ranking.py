class VentanaRanking(QWindow):
    def __init__(self) -> None:
        super().__init__()
        '''
        Front-end de la ventana mostrando los 5 mejores
        puntajes del juego
        '''
        #Label de título
        #Formulario de 5 label
        #QPushButton para volver
    
    def solicitud_volver(self) -> None:
        '''
        Método conectado al QPushButton volver, cierra
        la ventana de ranking
        '''

class FormularioPodio():

    senal_pedir_ranking = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        '''
        Ventana mostrando los 5 mejores puntajes
        del juego
        '''
        #5 Labels en un layout
        #llama a pedir_ranking

    def pedir_ranking(self) -> None:
        '''
        Usa la senal_pedir_ranking para indicar a
        la lógica que cargue el ranking
        '''

    def recibir_ranking(self, lista_ranking) -> None:
        '''
        Recibe la senal_cargar_formulario para setear
        los label del formulario
        '''

class LogicaVentanaRanking():

    senal_cargar_formulario = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        '''
        back-end de la ventana ranking, se encarga de
        leer el archivo txt y llenar los qlabels de esta
        '''
    def extraer_lugares(self) -> list:
        '''
        lee el archivo en la ruta RUTA_RANKING, que contiene
        los puntajes de los mejores puntajes y sus usuarios
        retorna una lista de tuples, que contienen los puntajes
        y usuarios de los mejores jugadores. La posición n de la 
        lista corresponde a la n+1 en el ranking 
        '''
    def cargar_formulario(self) -> None:
        '''
        extrae los lugares desde extraer lugares, y los envía
        mediante senal_cargar_formulario al formulario, para llenar
        los labels, si hay menos de 5 puntajes, se llena hasta las 5
        posiciones con ("Jugador malo", 0)
        '''