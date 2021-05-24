class VentanaInicio(QWindow):
    def __init__(self):

        senal_solicitar_partida = pyqtSignal(str)
        senal_abrir_ranking = pyqtSignal()

        super().__init__()
        '''
        Front-end de la ventana en la cual el jugador inicia
        el programa y puede iniciar un nuevo juego, como también
        ingresar a la ventana de rankings
        '''
        #QLineEdit para ingresar el nombre del jugador
        #QPushButton para iniciar una nueva partida con el nombre del lineedit
        #QPushButton para entrar a la ventana de rankings
    
    def boton_iniciar_partida(self):
        '''
        Método conectado al botón iniciar partida, manda la senal
        senal_solicitar_partida a requerimiento_ver_ranking de la lógica,
        '''
    
    def boton_abrir_ranking(self):
        '''
        Método conectado al botón ver ranking, manda la senal
        senal_abrir_ranking a comprobar_alfanum de la lógica,
        enviando el text del QLineEdit
        '''

class MensajeDeError():
    def __init__(self):
        '''
        Ventana que contiene un mensaje de error, que puede cerrarse
        '''

class LogicaVentanaInicio(algo):

    senal_inicio_partida = pyqtSignal()

    def __init__(self):
        '''
        Back-end de la ventana ventana inicio, esta comprueba
        que el nombre de usuario cumpla con la restricción. En
        el caso positivo, cierra ventana inicio, y abre ventana de
        preparación. De lo contrario, abre un message de error
        '''
    def comprobar_alfanum(self, usuario) -> bool:
        '''
        Recibe la senal_iniciar_partida y
        Comprueba que lo ingresado en el QLineEdit es correcto
        '''
    def ingreso_correcto(self) -> None:
        '''
        Envia la senal senal_inicio_partida a
        el frontend de VentanaInicio, para cerrar la ventana inicio,
        y a VentanaPreparacion para abrir la ventana de preparación
        '''
    def mensaje_error(self) -> None:
        '''
        Abre el mensaje de error
        '''
    def requerimiento_ver_ranking(self) -> None:
        '''
        Abre la ventana de ranking mediante la señal
        senal_abrir_ranking ¿y cierra la de inicio?
        '''
