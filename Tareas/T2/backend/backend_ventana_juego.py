from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication
import parametros as p
from backend.personajes import Personaje, Gorgory
from random import randint
import backend.utils as f


class LogicaVentanaJuego(QObject):

    senal_enviar_actualizacion_tablero = pyqtSignal(int, int, float, int)
    senal_cargar_tablero = pyqtSignal()

    senal_cambiar_pos_personaje = pyqtSignal(str)
    senal_inicializar_ventana = pyqtSignal(str, Personaje, int, str, int)
    senal_dar_obstaculos = pyqtSignal(list)
    senal_generar_objeto = pyqtSignal(str, tuple)
    senal_desaparecer_objeto = pyqtSignal(int)
    senal_pasar_tiempo = pyqtSignal(int)

    senal_mover_gorgory = pyqtSignal(tuple)
    senal_animacion_gorgory = pyqtSignal(str)

    senal_cambiar_boton_pausa = pyqtSignal()
    senal_esconder_ventana = pyqtSignal()
    senal_abrir_ventana_post_ronda = pyqtSignal(int, int, int, float)
    
    def __init__(self) -> None:
        super().__init__()
        '''
        Este es el backend de la ventana juego, y se encarga de
        realizar los procesos de esta
        '''
        self.rectangulo_mapa = p.RECTANGULO_TABLERO_JUEGO
    
    # ------------------ Aquí empieza una pseudo inicialización (cada vez que se entra)

    def abrir_juego(self, edificio, personaje, numero_ronda, dificultad):
        '''
        Este método se encargará de leer el progreso de la partida
        cuando es llamado, y enviar la información al frontend 
        mediante la señal senal_enviar_actualizacion_tablero
        Además carga los objetos
        '''
        # Seteamos los atributos de la ventana

        self.items_buenos = 0
        self.items_normales = 0
        self.items_malos = 0
        self.puntaje = 0
        self.edificio = edificio
        self.personaje = personaje
        self.gorgory = Gorgory(dificultad, self.personaje.nombre) # Se crea a Gorgory
        
        self.objetos = [] # Lista de objetos
        self.pausa = False # Almacena el estado de pausa
        self.terminado = False # Almacena si el juego ya acabó
        self.habilidad_especial_homero = False # Guarda si está activa la hab. especial
        self.habilidad_homero_ultima_vez = 0 # Guarda cuándo se usó la hab. especial

        # Tiempo que dura la ventana hasta que se acaba el juego
        if dificultad == "intro":
            tiempo = p.DURACION_INTRO
        elif dificultad == "avanzada":
            tiempo = p.DURACION_AVANZADA
        self.tiempo = tiempo
        
        # Posicion del personaje
        r = self.rectangulo_mapa
        pos = (randint(r[0], r[0] + r[2]), randint(r[1], r[1] + r[3]))

        #Inicializamos la ventana en el personaje
        self.personaje.inicializador_de_mapa("juego", self.rectangulo_mapa, pos, dificultad)
        #Le damos la posición inical a Gorgory
        self.gorgory.dar_posicion_inicial(pos)
        
        # Inicializamos el frontend con los datos correspondientes
        self.senal_inicializar_ventana.emit(edificio, personaje, numero_ronda, dificultad, tiempo)
        #Creamos el generador de objetos
        self.generador = f.Generador_de_objetos(self.personaje.nombre, dificultad)

        self.tiempo_juego = QTimer() # Reloj de ventana
        self.tiempo_juego.timeout.connect(self.pasar_tiempo)
        self.tiempo_juego.setInterval(1000*1)
        self.tiempo_juego.start()
        #
        self.conexiones()

    def conexiones(self):
        self.generador.senal_entregar_objeto.connect(self.recibir_objeto)
        self.personaje.senal_no_vida.connect(self.terminar_juego)
        self.gorgory.senal_animacion_gorgory.connect(self.animacion_gorgory)
        self.gorgory.senal_mover_gorgory.connect(self.mover_gorgory)
        self.gorgory.start() # Se inicia la animación de Gorgory

    # ------------------ Desde aquí se envían las actualizaciones al tablero
    
    def enviar_actualizacion_tablero(self):
        '''
        Este método se encargará de leer el progreso de la partida
        cuando es llamado y enviar la información al frontend 
        mediante la señal senal_enviar_actualizacion_tablero.
        '''
        a = self.items_buenos
        b = self.items_malos
        c = self.personaje.vida
        d = self.puntaje
            
        self.senal_enviar_actualizacion_tablero.emit(a, b, c, d)
    
    # ------------------- Acá empieza el trabajo de objetos

    def recibir_objeto(self, objeto):
        '''
        Recibe los objetos del generador de objetos
        '''
        self.objetos.append(objeto)
        objeto.aparecer(len(self.objetos) - 1)
        objeto.senal_desaparecer.connect(self.desaparecer_objeto)
        self.generar_objeto()

    def generar_objeto(self):
        '''
        Este método busca una posicion para el objeto si lo llama
        recibir objeto del backend. En caso de que no se haya podido poner,
        lo llama recibir objeto, pero del frontend
        '''
        r = self.rectangulo_mapa
        posicion = (randint(r[0], r[0] + r[2]), randint(r[1], r[1] + r[3]))
        path_objeto = self.objetos[-1].obtener_path()
        #print(path_objeto)
        self.senal_generar_objeto.emit(path_objeto, posicion)
    
    def objeto_tocado(self, indice):
        '''
        Recibe el índice de un objeto tocado y hace con él lo que corresponde
        '''
        objeto = self.objetos[indice]
        objeto.senal_desaparecer.disconnect()
        que_hacer = objeto.dar_efecto()

        if objeto.tipo == "peligroso":
            self.items_malos += 1
        elif objeto.tipo == "x2" or objeto.tipo == "vida":
            self.items_buenos += 1
        else:
            self.items_normales += 1
        if que_hacer[0] == "vida":
            self.personaje.vida += que_hacer[1]
        elif que_hacer[0] == "puntaje":
            self.puntaje += que_hacer[1]
        else:
            raise ValueError("error al sumar objeto")

        # ---------------------- Habilidad homero

        if self.personaje.nombre == "homero" and self.items_normales % 10 == 0:
            if self.items_normales != 0 and self.items_normales != self.habilidad_homero_ultima_vez:
                self.habilidad_homero_ultima_vez = self.items_normales
                self.habilidad_especial_homero = True
                self.personaje.vida += p.PONDERADOR_VIDA_HOMERO
        if self.habilidad_especial_homero and objeto.tipo == "peligroso":
            self.habilidad_especial_homero = False
            self.items_malos = 0
        elif self.habilidad_especial_homero and (objeto.tipo == "x2" or objeto.tipo == "vida"):
            self.habilidad_especial_homero = False
            self.items_buenos -= 1

        # ----------------------- 

        self.enviar_actualizacion_tablero()

    def desaparecer_objeto(self, indice):
        '''
        Desaparece un objeto cuando se acaba su tiempo de vida
        '''
        self.objetos[indice].senal_desaparecer.disconnect()
        self.senal_desaparecer_objeto.emit(indice)

    # --------------------------------- Desde acá se manejan los obstáculos

    def generar_obstaculos(self):
        self.posiciones_obstaculos = list()
        for _ in range(3):
            misma_posicion = True
            while misma_posicion:
                misma_posicion = False
                r = self.rectangulo_mapa
                nuevo_obstaculo = (randint(r[0], r[0] + r[2]), randint(r[1] + 5, r[1] + r[3] + 5))
                # Se hace un ajuste de +5, ya que los límites están hecho de acuerdo a donde se
                # puede mover el personaje, y como los obstáculos son más pequeños, sus patas
                # no alcanzan a estar dentro del mapa
                for obstaculo in self.posiciones_obstaculos:
                    if (obstaculo[0] - nuevo_obstaculo[0])**2 <= 160**2 and\
                        (obstaculo[1] - nuevo_obstaculo[1])**2 <= 160**2:
                        misma_posicion = True
            self.posiciones_obstaculos.append(nuevo_obstaculo)
        dict_rutas = p.RUTAS_OBSTACULOS[self.edificio]
        lista_rutas = list(dict_rutas.values())
        lista_final = list(zip(lista_rutas, self.posiciones_obstaculos))
        self.senal_dar_obstaculos.emit(lista_final)
    
    # -------------------------------- Manaje el tiempo de la partida

    def pasar_tiempo(self):
        '''
        Este método es llamado por el QTimer que cambia el tiempo de juego
        '''
        self.tiempo -= 1
        if self.tiempo > 0:
            self.senal_pasar_tiempo.emit(self.tiempo)
        else:
            self.terminar_juego()

    # -------------------- Lo de aquí en adelante es para Gorgory

    def guardar_posicion_personaje(self, posicion):
        '''
        Recibe las posiciones históricas del personaje principal
        y las manda a Gorgory
        '''
        self.gorgory.recibir_posicion(posicion)

    def animacion_gorgory(self, path_dado):
        '''
        Recibe las actualizaciones de animación de Gorgory y las manda al frontend
        '''
        self.senal_animacion_gorgory.emit(path_dado)

    def mover_gorgory(self, posicion):
        '''
        Recibe las actualizaciones de movimiento de Gorgory y las manda al frontend
        '''
        self.senal_mover_gorgory.emit(posicion)

    def gorgory_intersectado(self):
        '''
        Recibe una señal del frontend si Gorgory intersectó con el personaje
        '''
        self.personaje.vida = 0
        self.terminar_juego()

    # ------------------------------- Otros

    def pausa_juego(self):
        '''
        Este método se encarga de, cuando es llamado,
        reanudar el juego si está pausado y pausarlo si no 
        mediante la señal senal_enviar_actualizacion_tablero.
        '''
        if not self.pausa:
            self.tiempo_juego.stop()
            self.generador.parar()
            self.personaje.timer.stop()
            for objeto in self.objetos:
                objeto.pausar()
            self.pausa = True
            self.gorgory.pausar()
        else:
            self.tiempo_juego.start()
            self.generador.iniciar()
            self.personaje.timer.start()
            for objeto in self.objetos:
                objeto.reanudar()
            self.pausa = False
            self.gorgory.pausar()

    def terminar_juego(self):
        '''
        Este método se encarga de, cuando es llamado,
        salir del juego y llevar a la ventana post ronda
        '''
        if not self.terminado:
            # Desconecta todo lo necesario
            self.terminado = True
            self.tiempo_juego.stop()
            self.generador.parar()
            self.personaje.timer.stop()
            self.gorgory.timer.stop()
            self.gorgory.senal_animacion_gorgory.disconnect()
            self.gorgory.senal_mover_gorgory.disconnect()
            for objeto in self.objetos:
                objeto.pausar()
            self.pausa = True
            
            self.senal_esconder_ventana.emit()
            #
            a = self.puntaje * self.personaje.vida
            b = self.items_buenos
            c = self.items_malos
            d = self.personaje.vida
            self.senal_abrir_ventana_post_ronda.emit(a, b, c, d)
        else:
            print("traté de terminar el juego, pero no se pudo")

    def salir_juego(self):
        '''
        Este método cierra el programa por el botón
        '''
        QApplication.quit()

    def cheats(self, combinacion):
        '''
        Comprueba si se ejecutó algún cheat, y los ejecuta
        '''
        if "v" in combinacion and "i" in combinacion and "d" in combinacion:
            self.personaje.vida += p.VIDA_TRAMPA
            self.enviar_actualizacion_tablero()
        elif "v" in combinacion and "i" in combinacion and "n" in combinacion:
            self.terminar_juego()
