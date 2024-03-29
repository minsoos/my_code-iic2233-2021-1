from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import parametros as p
import random


def ordenar_por_puntaje(objeto):
    '''
    Esta función ordena por puntaje listas del tipo que se retornan
    de readlines del archivo ranking.txt
    '''
    return objeto[1]


class Objeto(QObject):

    senal_desaparecer = pyqtSignal(int)

    def __init__(self, tipo, nombre_personaje, dificultad) -> None:
        super().__init__()
        self.tipo = tipo
        self.vencido = False
        self.personaje = nombre_personaje
        self.rutas = p.RUTAS_OBJETOS
        self.posicion_en_lista = None

        # Dependiendo de la dificultad le da una duración vivo
        if dificultad == "intro":
            self.duracion = p.TIEMPO_OBJETO_INTRO
        elif dificultad == "avanzada":
            self.duracion = p.TIEMPO_OBJETO_AVANZADA
        else:
            raise ValueError("en definicón de objeto")
        if nombre_personaje == "lisa" and tipo == "normal":
            self.duracion += p.PONDERADOR_TIEMPO_LISA

        # Hace que pase el tiempo cada un segundo
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.comprobar_tiempo)
        self.tiempo_pasado = 0 # Almacena el tiempo actual
    
    def obtener_path(self):
        '''
        Obtiene el path del objeto
        '''
        if self.tipo == "peligroso":
            return self.rutas["peligroso"]
        elif self.tipo == "vida":
            return self.rutas["vida"]
        elif self.tipo == "x2":
            return self.rutas[self.personaje]["x2"]
        elif self.tipo == "normal":
            return self.rutas[self.personaje]["normal"]
        else:
            raise ValueError("en obtener_path en objeto")
    
    def reanudar(self):
        self.timer.start()
    
    def pausar(self):
        self.timer.stop()
    
    def dar_efecto(self):
        '''
        Retorna info. con el efecto que tiene el objeto
        '''
        if self.tipo == "peligroso":
            return ("vida", -1 * p.PONDERADOR_VENENO)
        elif self.tipo == "vida":
            return ("vida", p.PONDERADOR_CORAZON)
        elif self.tipo == "x2":
            return ("puntaje", p.PUNTOS_OBJETO_NORMAL * 2)
        elif self.tipo == "normal":
            return ("puntaje", p.PUNTOS_OBJETO_NORMAL)

    def aparecer(self, posicion_en_lista):
        '''
        Empieza su timer de autodestrucción (cuando "vence") y le da la posición
        que tiene en la lista de objetos
        '''
        self.posicion_en_lista = posicion_en_lista
        self.timer.start()

    def comprobar_tiempo(self):
        '''
        Comprueba si ya pasó el tiempo que debe durar
        '''
        if self.tiempo_pasado >= self.duracion:
            if self.vencido:
                self.timer.stop()
            else:
                self.senal_desaparecer.emit(self.posicion_en_lista)
                vencido = True
        self.tiempo_pasado +=1


class Generador_de_objetos(QObject):

    senal_entregar_objeto = pyqtSignal(object)

    def __init__(self, nombre_personaje, dificultad) -> None:
        super().__init__()
        self.personaje = nombre_personaje
        self.dificultad = dificultad
        self.lista_objetos = []
        
        # Da el periodo en que se generan los objetos
        if dificultad == "intro":
            periodo = p.APARICION_INTRO*1000
        elif dificultad == "avanzada":
            periodo = p.APARICION_AVANZADA*1000
        if self.personaje == "moe":
            periodo /= 2
        
        # Inicia el generador a partir de ese tiempo
        self.timer = QTimer()
        self.timer.setInterval(periodo)
        self.timer.timeout.connect(self.generar_objeto)
        self.iniciar()
    
    def iniciar(self):
        self.timer.start()
    
    def parar(self):
        self.timer.stop()

    def generar_objeto(self):
        '''
        Genera un objeto de acuerdo a sus probabilidades
        '''
        numero_a_comparar = random.uniform(0, 1)
        #
        if 0 <= numero_a_comparar < p.PROB_BUENO:
            numero_a_comparar = random.randint(0,1)
            if numero_a_comparar == 0:
                objeto = Objeto("x2", self.personaje, self.dificultad)
            elif numero_a_comparar == 1:
                objeto = Objeto("vida", self.personaje, self.dificultad)

        elif p.PROB_BUENO <= numero_a_comparar < p.PROB_BUENO + p.PROB_NORMAL:
            numero_a_comparar = random.randint(0,1)
            objeto = Objeto("normal", self.personaje, self.dificultad)

        else:
            objeto = Objeto("peligroso", self.personaje, self.dificultad)

        # Entrega al objeto al backend del juego
        self.senal_entregar_objeto.emit(objeto)
