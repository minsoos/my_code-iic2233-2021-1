import sys
from ventana_preparacion import LogicaVentanaPreparacion, VentanaPreparacion
from ventana_ranking import LogicaVentanaRanking, VentanaRanking

from PyQt5.QtWidgets import QApplication

import parametros as p
from ventana_de_inicio import VentanaError, VentanaInicio, LogicaVentanaInicio
from ventana_preparacion import VentanaPreparacion, LogicaVentanaPreparacion, VentanaMapaErrado
from ventana_juego import VentanaJuego, LogicaVentanaJuego
from ventana_postronda import VentanaPostRonda, LogicaVentanaPostRonda
from musica import Musica
###Hay que crear el ranking.txt si no existe


def hook(type_error, traceback):
    print(type_error)
    print(traceback)

open("ranking.txt", "a")

if __name__ == "__main__":
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    # --------------------------Ventana inicio
    ventana_inicio = VentanaInicio()
    logica_ventana_inicio = LogicaVentanaInicio()
    musica = Musica()
    musica.timer.start()
    # Señales
    ventana_inicio.senal_solicitar_partida.connect(logica_ventana_inicio.comprobar_alfanum)
    ventana_inicio.senal_abrir_ranking.connect(logica_ventana_inicio.requerimiento_ver_ranking)
    logica_ventana_inicio.senal_inicio_partida.connect(ventana_inicio.inicio_partida)
    # ---------------------------Ventana error
    ventana_inicio_error = VentanaError()
    # Señales
    logica_ventana_inicio.senal_ventana_error.connect(ventana_inicio_error.mostrar)
    # ----------------------------Ventana ranking
    ventana_ranking = VentanaRanking()
    logica_ventana_ranking = LogicaVentanaRanking()
    # Señales
    ventana_inicio.senal_abrir_ranking.connect(ventana_ranking.mostrar)
    ventana_ranking.senal_pedir_actualizar.connect(logica_ventana_ranking.extraer_lugares)
    logica_ventana_ranking.senal_cargar_puntajes.connect(ventana_ranking.actualizar)
    # ----------------------------- Ventana preparación partida
    ventana_preparacion = VentanaPreparacion()
    logica_ventana_preparacion = LogicaVentanaPreparacion()
    ventana_mapa_errado = VentanaMapaErrado()
    # Señales
    conexion_n = logica_ventana_preparacion.iniciar_nueva_partida
    logica_ventana_inicio.senal_inicio_partida.connect(conexion_n)
    conexion_n = logica_ventana_preparacion.iniciar_nueva_partida
    conexion_n = ventana_preparacion.actualizar_info
    logica_ventana_preparacion.senal_actualizar_info_ventana.connect(conexion_n)
    conexion_n = logica_ventana_preparacion.cambiar_personaje
    ventana_preparacion.senal_solicitud_cambiar_personaje.connect(conexion_n)
    conexion_n = ventana_preparacion.actualizar_animacion_personaje
    logica_ventana_preparacion.senal_actualizar_animacion_personaje.connect(conexion_n)
    conexion_n = ventana_preparacion.actualizar_movimiento_personaje
    logica_ventana_preparacion.senal_actualizar_movimiento_personaje.connect(conexion_n)
    conexion_n = logica_ventana_preparacion.movimiento_de_personaje_solicitado
    ventana_preparacion.senal_tecla_presionada_mover.connect(conexion_n)
    conexion_n = ventana_preparacion.ocultar_ventana
    logica_ventana_preparacion.senal_ocultar_ventana.connect(conexion_n)
    conexion_n = logica_ventana_preparacion.revision_solicitud_entrada_a_edificio
    ventana_preparacion.senal_solicitud_entrar_edificio.connect(conexion_n)
    logica_ventana_preparacion.senal_abrir_ventana_error.connect(ventana_mapa_errado.mostrar)
    logica_ventana_preparacion.senal_mostrar_ventana.connect(ventana_preparacion.mostrar_ventana)
    ventana_preparacion.senal_boton_salir.connect(logica_ventana_preparacion.boton_salir_presionado)
    ventana_preparacion.senal_boton_salir.connect(ventana_inicio.mostrar)
    # ---------------------------- Ventana juego
    ventana_juego = VentanaJuego()
    logica_juego = LogicaVentanaJuego()
    logica_ventana_preparacion.senal_abrir_ventana_juego.connect(logica_juego.abrir_juego)
    ventana_juego.senal_pausa_juego.connect(logica_juego.pausa_juego)
    ventana_juego.senal_salir_juego.connect(logica_juego.salir_juego)
    ventana_juego.senal_tecla_presionada_cheat.connect(logica_juego.cheats)
    logica_juego.senal_generar_objeto.connect(ventana_juego.recibir_objeto)
    ventana_juego.senal_pedir_objeto.connect(logica_juego.generar_objeto)
    #Esto lo hice hoy, 29/05/21
    logica_juego.senal_inicializar_ventana.connect(ventana_juego.inicializar)
    logica_juego.senal_dar_obstaculos.connect(ventana_juego.crear_obstaculos)
    ventana_juego.senal_pedir_crear_obstaculos.connect(logica_juego.generar_obstaculos)
    ventana_juego.senal_objeto_tocado.connect(logica_juego.objeto_tocado)
    logica_juego.senal_desaparecer_objeto.connect(ventana_juego.desaparecer_objeto)
    logica_juego.senal_enviar_actualizacion_tablero.connect(ventana_juego.actualizar_tablero)
    logica_juego.senal_pasar_tiempo.connect(ventana_juego.pasar_tiempo)
    logica_juego.senal_esconder_ventana.connect(ventana_juego.esconder_ventana)
    ventana_juego.senal_personaje_movido.connect(logica_juego.guardar_posicion_personaje)
    logica_juego.senal_mover_gorgory.connect(ventana_juego.mover_gorgory)
    logica_juego.senal_animacion_gorgory.connect(ventana_juego.animacion_gorgory)
    ventana_juego.senal_acabar_juego.connect(logica_juego.gorgory_intersectado)
    # ----------------------------- Ventana postronda
    ventana_post_ronda = VentanaPostRonda()
    logica_post_ronda = LogicaVentanaPostRonda()
    logica_juego.senal_abrir_ventana_post_ronda.connect(logica_post_ronda.inicializar_ventana)
    logica_post_ronda.senal_inicializar.connect(ventana_post_ronda.inicializar_ventana)
    ventana_post_ronda.senal_continuar.connect(logica_post_ronda.continuar_juego)
    ventana_post_ronda.senal_salir.connect(logica_post_ronda.salir)
    ventana_post_ronda.senal_salir_inicio.connect(logica_post_ronda.salir_a_inicio)
    logica_post_ronda.senal_volver_preparacion.connect(logica_ventana_preparacion.volver_a_ventana)
    logica_post_ronda.senal_abrir_inicio.connect(ventana_inicio.mostrar)
    logica_post_ronda.senal_guardar_progreso.connect(logica_ventana_preparacion.guardar_y_salir)

    app.exec()