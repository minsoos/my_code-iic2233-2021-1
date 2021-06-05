from os.path import join

# -------------------Personajes

VELOCIDAD_HOMERO = 8
PONDERADOR_VIDA_HOMERO = 0.5
VELOCIDAD_LISA = 8
PONDERADOR_TIEMPO_LISA = 5
VELOCIDAD_MOE = 8
VELOCIDAD_KRUSTY = 8
TIEMPO_DELAY_AVANZADA = 5
TIEMPO_DELAY_INTRO = 10
TAMANO_PERSONAJES_PREPARACION = (20, 40)
TAMANO_PERSONAJES_JUEGO = (30, 50)
# ------------ PARAMETROS DE LAS VENTANAS

RECTANGULO_TABLERO_PREPARACION = (8, 520, 870, 115)
RECTANGULO_TABLERO_JUEGO = (5, 245, 1063, 619-251+10)
TIEMPO_ENTRE_MENSAJES_DE_ERROR = 2
POSICION_DESAPARECER_PERSONAJE = (-50, -50)
TAMANO_OBSTACULOS = (30, 40)
TAMANO_OBJETOS = (30, 40)



#Personaje enemigo (Jefe Gorgory)##########
#TIEMPO_DELAY_{DIFICULTAD} = None

#Configuración rondas
DURACION_INTRO = 60
DURACION_AVANZADA = 10

# ---------------------- Objetos

TIEMPO_OBJETO_INTRO = 10
TIEMPO_OBJETO_AVANZADA = 20
APARICION_INTRO = 2
APARICION_AVANZADA = 5

#cheatscodes
VIDA_TRAMPA = 0.35

#--------------------------- Paths

RUTA_CEREBRO_HOMERO = join("frontend", "sprites", "cerebro_homero.jpg")
# fuente: https://www.vix.com/es/series/189634/me-dijeron-lento-las-13-mejores-conversaciones-que-homero-tuvo-con-su-cerebro
RUTA_ESTRANGULACION = join("frontend", "sprites", "homero_estrangulando_a_bart.jpg")
# fuente: https://lanetaneta.com/lo-peor-que-homer-simpson-ha-hecho-clasificado-screenrant/
RUTA_FOTO_POSTRONDA = join("frontend", "sprites", "foto_postronda.jpg")
# fuente: https://www.buzzfeed.com/mx/mireyagonzalez/memes-de-la-peda
RUTA_LOGO_INICIO = join("frontend", "sprites", "logo_inicio.png")
RUTA_LOGO_RANKING = join("frontend", "sprites", "logo_ranking.png")
RUTA_RANKING = join("ranking.txt")
RUTA_MUSICA = join("canciones", "musica.wav")

#---------------------- Designer

DISENO_VENTANA_INICIO = join("frontend", "assets", "ventana_inicio.ui")
DISENO_VENTANA_ERROR = join("frontend", "assets", "ventana_de_error.ui")
DISENO_VENTANA_RANKING = join("frontend", "assets", "ventana_ranking.ui")
DISENO_VENTANA_PREPARACION = join("frontend", "assets", "ventana_preparacion.ui")
DISENO_VENTANA_MAPA_ERRADO = join("frontend", "assets", "ventana_mapa_errado.ui")
DISENO_VENTANA_JUEGO = join("frontend", "assets", "ventana_juego.ui")
DISENO_VENTANA_POSTRONDA = join("frontend", "assets", "ventana_postronda.ui")
DISENO_VENTANA_PREPARACION_ANTIGUA = join("frontend", "assets", "ventana_preparacion_antigua.ui")
# ------------------- Diccionario de rutas

RUTAS_MADRE = {
    "planta": join("frontend", "sprites", "Mapa", "Planta_nuclear"),
    "krustyland": join("frontend", "sprites", "Mapa", "Krustyland"),
    "bar": join("frontend", "sprites", "Mapa", "Bar"),
    "preparacion": join("frontend", "sprites", "Mapa", "Mapa_Preparación"),
    "primaria": join("frontend", "sprites", "Mapa", "Primaria")
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
    "homero": join("frontend", "sprites", "Personajes", "Homero"),
    "lisa": join("frontend", "sprites", "Personajes", "Lisa"),
    "krusty": join("frontend", "sprites", "Personajes", "Krusty"),
    "gorgory": join("frontend", "sprites", "Personajes", "Gorgory"),
    "moe": join("frontend", "sprites", "Personajes", "Moe")
}


RUTAS_VENTANA_PREPARACION = {
    "homero": join("frontend", "sprites", "Personajes", "Homero", "down_3.png"),
    "lisa": join("frontend", "sprites", "Personajes", "Lisa", "down_1.png"),
    "krusty": join("frontend", "sprites", "Personajes", "Krusty", "down_1.png"),
    "moe": join("frontend", "sprites", "Personajes", "Moe", "down_1.png"),
    "logo": RUTA_LOGO_INICIO,
    "fondo": join(RUTAS_MADRE["preparacion"], "Fondo.png"),
    "planta": join(RUTAS_MADRE["preparacion"],"PlantaNuclear.png"),
    "bar": join(RUTAS_MADRE["preparacion"],"Bar.png"),
    "krustyland": join(RUTAS_MADRE["preparacion"],"Krustyland.png"),
    "primaria": join(RUTAS_MADRE["preparacion"],"Primaria.png")
}

# -------------------------- Objetos

RUTAS_OBJETOS_HOMERO = {
    "normal": join("frontend", "sprites", "Objetos", "Dona.png"),
    "x2": join("frontend", "sprites", "Objetos", "DonaX2.png")
}
RUTAS_OBJETOS_LISA = {
    "normal": join("frontend", "sprites", "Objetos", "Saxofon.png"),
    "x2": join("frontend", "sprites", "Objetos", "SaxofonX2.png")
}
RUTAS_OBJETOS_MOE = {
    "normal": join("frontend", "sprites", "Objetos", "Cerveza.png"),
    "x2": join("frontend", "sprites", "Objetos", "CervezaX2.png")
}
RUTAS_OBJETOS_KRUSTY = {
    "normal": join("frontend", "sprites", "Objetos", "Krusty.png"),
    "x2": join("frontend", "sprites", "Objetos", "KrustyX2.png")
}
RUTAS_OBJETOS = {
    "peligroso": join("frontend", "sprites", "Objetos", "Veneno.png"),
    "vida": join("frontend", "sprites", "Objetos", "Corazon.png"),
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


#Objetos normales
PROB_NORMAL = 0.6
PUNTOS_OBJETO_NORMAL = 20

#Objetos buenos

PROB_BUENO = 0.2
PONDERADOR_CORAZON = 0.4

#Objetos peligrosos
PROB_VENENO = 0.2
PONDERADOR_VENENO = 0.3
# ------------ Para que funcione, las probabilidades deben sumar 1
