import parametros as p
from PyQt5.QtCore import QObject, pyqtSignal
import backend.utils as f


class LogicaVentanaRanking(QObject):

    senal_cargar_puntajes = pyqtSignal(list)

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
        with open(p.RUTA_RANKING, encoding="UTF-8") as archivo:
            lista = archivo.readlines()
            lista = map(lambda x: list(x.strip().split(",")), lista)
            lista = list(map(lambda x: (x[0], int(x[1])), lista))
        lista.sort(key=f.ordenar_por_puntaje, reverse=True)
        self.cargar_lugares(lista)

    def cargar_lugares(self, lista) -> None:
        '''
        extrae los lugares desde extraer lugares, y los envía
        mediante senal_cargar_formulario al formulario, para llenar
        los labels, si hay menos de 5 puntajes, se llena hasta las 5
        posiciones con ("Jugador malo", 0)
        '''
        self.senal_cargar_puntajes.emit(lista)