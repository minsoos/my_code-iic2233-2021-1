from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication


class LogicaVentanaPostRonda(QObject):

    senal_inicializar = pyqtSignal(int, int, int, int, bool)
    senal_abrir_inicio = pyqtSignal()
    senal_volver_preparacion = pyqtSignal(int, int, int)
    senal_guardar_progreso = pyqtSignal(int, int, int)

    def __init__(self) -> None:
        super().__init__()
        '''
        Este es el backend de la ventana post ronda
        '''

    def salir(self):
        '''
        Te saca del programa
        '''
        self.guardar_progreso()
        QApplication.quit()

    def salir_a_inicio(self):
        '''
        Te lleva a la ventana de inicio y cierra la actual
        '''
        self.guardar_progreso()
        self.senal_abrir_inicio.emit()
        

    def continuar_juego(self):
        '''
        Te lleva a la ventana de preparación y cierra la actual
        '''
        self.senal_volver_preparacion.emit(self.puntaje, self.i_buenos, self.i_malos)
    
    def guardar_progreso(self):
        self.senal_guardar_progreso.emit(self.puntaje, self.i_buenos, self.i_malos)
    
    def inicializar_ventana(self, puntaje, i_buenos, i_malos, vida):
        vida = vida * 100
        self.vida = vida
        self.puntaje = puntaje
        self.i_buenos = i_buenos
        self.i_malos = i_malos
        if vida > 0:
            perdio = False
        else:
            perdio = True
        self.senal_inicializar.emit(puntaje, i_buenos, i_malos, vida, perdio)