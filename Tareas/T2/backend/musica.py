import parametros as p
from PyQt5.QtCore import QThread
from PyQt5 import QtMultimedia


class Musica(QThread):
    # Base de actividad AS2

    def __init__(self):
        super().__init__()
        self.ruta_cancion = p.RUTA_MUSICA
        # self.timer = QTimer()
        # self.timer.setInterval(1000*128)
        # self.timer.timeout.connect(self.comenzar)
        # self.comenzar()
        # self.timer.start()
        self.empezar()
        self.pausado = False

    def empezar(self, *args, **kwargs):
        self.cancion = QtMultimedia.QSound(self.ruta_cancion)
        self.cancion.setLoops(-1)
        # Fuente: https://www.programmersought.com/article/37923092494/
        self.cancion.play()
    
    def pausar(self):
        if self.pausado:
            self.pausado = False
            self.cancion.play()
        else:
            self.pausado = True
            self.cancion.stop()