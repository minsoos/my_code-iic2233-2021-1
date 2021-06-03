from os.path import join
from PyQt5 import uic

# -------------------Personajes

VELOCIDAD_HOMERO = None
PONDERADOR_VIDA_HOMERO = None
VELOCIDAD_LISA = None
PONDERADOR_TIEMPO_LISA = -8
VELOCIDAD_PRUEBA = 8

# ------------ PARAMETROS DE LAS VENTANAS

POSICION_INICIAL_VENTANA_PREPARACION = (50, 550)
RECTANGULO_TABLERO_PREPARACION = (8, 480, 870, 155)
RECTANGULO_TABLERO_JUEGO = (5, 245, 1063, 619-251+10)



#Personaje enemigo (Jefe Gorgory)##########
#TIEMPO_DELAY_{DIFICULTAD} = None

#Configuración rondas
DURACION_INTRO = 90
DURACION_AVANZADA = 30

#cheatscodes
VIDA_TRAMPA = None

#--------------------------- Paths

RUTA_CEREBRO_HOMERO = join("sprites", "cerebro_homero.jpg")
# fuente: https://www.vix.com/es/series/189634/me-dijeron-lento-las-13-mejores-conversaciones-que-homero-tuvo-con-su-cerebro
RUTA_ESTRANGULACION = join("sprites", "homero_estrangulando_a_bart.jpg")
# fuente: https://lanetaneta.com/lo-peor-que-homer-simpson-ha-hecho-clasificado-screenrant/
RUTA_FOTO_POSTRONDA = join("sprites", "foto_postronda.jpg")
# fuente: https://www.buzzfeed.com/mx/mireyagonzalez/memes-de-la-peda
RUTA_LOGO_INICIO = join("sprites", "logo_inicio.png")
RUTA_LOGO_RANKING = join("sprites", "logo_ranking.png")
RUTAS_RANKING = join("ranking.txt")

#---------------------- Designer

DISENO_VENTANA_INICIO = join("assets", "ventana_inicio.ui")
DISENO_VENTANA_ERROR = join("assets", "ventana_de_error.ui")
DISENO_VENTANA_RANKING = join("assets", "ventana_ranking.ui")
DISENO_VENTANA_PREPARACION = join("assets", "ventana_preparacion.ui")
DISENO_VENTANA_MAPA_ERRADO = join("assets", "ventana_mapa_errado.ui")
DISENO_VENTANA_JUEGO = join("assets", "ventana_juego.ui")
DISENO_VENTANA_POSTRONDA = join("assets", "ventana_postronda.ui")

# ------------------- Diccionario de rutas

RUTAS_MADRE = {
    "planta": join("sprites", "Mapa", "Planta_nuclear"),
    "krustyland": join("sprites", "Mapa", "Krustyland"),
    "bar": join("sprites", "Mapa", "Bar"),
    "preparacion": join("sprites", "Mapa", "Mapa_Preparación"),
    "primaria": join("sprites", "Mapa", "Primaria")
}
RUTAS_IMAGENES_JUEGO = {
    "mapa_planta": join(RUTAS_MADRE["planta"], "Mapa.png"),
    "logo": join("sprites", "Logo.png"),
    "mapa_krustyland": join(RUTAS_MADRE["krustyland"], "Mapa.png"),
    "mapa_bar": join(RUTAS_MADRE["bar"], "Mapa.png"),
    "mapa_preparacion": join(RUTAS_MADRE["preparacion"], "Mapa.png"),
    "mapa_primaria": join(RUTAS_MADRE["primaria"], "Mapa.png")
}
RUTAS_PERSONAJES = {
    "homero": join("sprites", "Personajes", "Homero"),
    "lisa": join("sprites", "Personajes", "Lisa"),
    "krusty": join("sprites", "Personajes", "Krusty"),
    "gorgory": join("sprites", "Personajes", "Gorgory"),
    "moe": join("sprites", "Personajes", "Moe")
}


RUTAS_VENTANA_PREPARACION = {
    "homero": join("sprites", "Personajes", "Homero", "down_3.png"),
    "lisa": join("sprites", "Personajes", "Lisa", "down_1.png"),
    "krusty": join("sprites", "Personajes", "Krusty", "down_1.png"),
    "moe": join("sprites", "Personajes", "Moe", "down_1.png"),
    "logo": RUTA_LOGO_INICIO,
    "fondo": join(RUTAS_MADRE["preparacion"], "Fondo.png"),
    "planta": join(RUTAS_MADRE["preparacion"],"PlantaNuclear.png"),
    "bar": join(RUTAS_MADRE["preparacion"],"Bar.png"),
    "krustyland": join(RUTAS_MADRE["preparacion"],"Krustyland.png"),
    "primaria": join(RUTAS_MADRE["preparacion"],"Primaria.png")
}

# -------------------------- Objetos

RUTAS_OBJETOS_HOMERO = {
    "normal": join("sprites", "Objetos", "Dona.png"),
    "x2": join("sprites", "Objetos", "DonaX2.png")
}
RUTAS_OBJETOS_LISA = {
    "normal": join("sprites", "Objetos", "Saxofon.png"),
    "x2": join("sprites", "Objetos", "SaxofonX2.png")
}
RUTAS_OBJETOS_MOE = {
    "normal": join("sprites", "Objetos", "Cerveza.png"),
    "x2": join("sprites", "Objetos", "CervezaX2.png")
}
RUTAS_OBJETOS_KRUSTY = {
    "normal": join("sprites", "Objetos", "Krusty.png"),
    "x2": join("sprites", "Objetos", "KrustyX2.png")
}
RUTAS_OBJETOS = {
    "peligroso": join("sprites", "Objetos", "Veneno.png"),
    "vida": join("sprites", "Objetos", "Corazon.png"),
    "homero": RUTAS_OBJETOS_HOMERO,
    "lisa": RUTAS_OBJETOS_LISA,
    "moe": RUTAS_OBJETOS_MOE,
    "krusty": RUTAS_OBJETOS_KRUSTY
}

# ------------------------ Obstáculos

RUTAS_OBSTACULOS_PLANTA = {
    "1": join(RUTAS_MADRE["planta"], "Obstaculo1.png"),
    "2": join(RUTAS_MADRE["planta"], "Obstaculo2.png"),
    "3": join(RUTAS_MADRE["planta"], "Obstaculo3.png")
}
RUTAS_OBSTACULOS_KRUSTYLAND = {
    "1": join(RUTAS_MADRE["krustyland"], "Obstaculo1.png"),
    "2": join(RUTAS_MADRE["krustyland"], "Obstaculo2.png"),
    "3": join(RUTAS_MADRE["krustyland"], "Obstaculo3.png")
}
RUTAS_OBSTACULOS_PRIMARIA = {
    "1": join(RUTAS_MADRE["primaria"], "Obstaculo1.png"),
    "2": join(RUTAS_MADRE["primaria"], "Obstaculo2.png"),
    "3": join(RUTAS_MADRE["primaria"], "Obstaculo3.png")
}
RUTAS_OBSTACULOS_BAR = {
    "1": join(RUTAS_MADRE["bar"], "Obstaculo1.png"),
    "2": join(RUTAS_MADRE["bar"], "Obstaculo2.png"),
    "3": join(RUTAS_MADRE["bar"], "Obstaculo3.png")
}
RUTAS_OBSTACULOS = {
    "planta": RUTAS_OBSTACULOS_PLANTA,
    "krustyland": RUTAS_OBSTACULOS_KRUSTYLAND,
    "primaria": RUTAS_OBSTACULOS_PRIMARIA,
    "bar": RUTAS_OBSTACULOS_BAR
}

# ------------------ Termina obstáculos

# ---------------------- Objetos

TIEMPO_OBJETO_INTRO = 10
TIEMPO_OBJETO_AVANZADA = 20
APARICION_INTRO = 5
APARICION_AVANZADA = 5

#Objetos normales

PUNTOS_OBJETO_NORMAL = 20
PROB_NORMAL = 0.3

#Objetos buenos

PROB_BUENO = 0.4
PONDERADOR_CORAZON = 0.4

#Objetos peligrosos

PONDERADOR_VENENO = 0.3
PROB_VENENO = 0.3
# ------------ Para que funcione, las probabilidades deben sumar 1
