from datetime import datetime
import menu_de_chats
from parametros import ABANDONAR_FRASE, VOLVER_FRASE
class Fecha:
    def __init__(self, ano, mes, dia, hora, minutos, segundos):
        self.ano = ano
        self.mes = mes
        self.dia = dia
        self.hora = hora
        self.minutos = minutos
        self.segundos = segundos

    def __str__(self):
        return f"{self.ano}/{self.mes}/{self.dia} {self.hora}:{self.minutos}:{self.segundos}"


class Mensaje:
    def __init__(self, tipo, emisor, receptor, fecha, contenido):
        self.tipo = tipo    
        self.emisor = emisor
        self.receptor = receptor
        self.fecha = fecha
        self.contenido = contenido
    def definir_fecha(self):
        self.fecha = self.fecha.split(" ")
        fecha = self.fecha[0].split("/")
        ano = int(fecha[0])
        mes = int(fecha[1])
        dia = int(fecha[2])
        hour = self.fecha[1].split(":")
        hora = int(hour[0])
        minutos = int(hour[1])
        segundos = int(hour[2])
        self.fecha = Fecha(ano, mes, dia, hora, minutos, segundos)


def ordenar_mensajes(mensaje):
    m = mensaje.fecha
    t = m.ano, m.mes, m.dia, m.hora, m.minutos, m.segundos
    return t


def abrir_chat(usuario, receptor, tipo):
    archivo_mensajes = open("mensajes.csv", encoding='utf8')
    mensajes = archivo_mensajes.readlines()
    archivo_mensajes.close()
    lista_mensajes = []
    for i in range(1, len(mensajes)):
        mensajes[i] = mensajes[i].strip().split(",")
        m = mensajes[i]
        mensaje = Mensaje(m[0], m[1], m[2], m[3], m[4])
        mensaje.definir_fecha()
        lista_mensajes.append(mensaje)
    if tipo == "regular":
        abrir_chat_regular(usuario, receptor, lista_mensajes)
    elif tipo == "grupo":
        abrir_chat_grupal(usuario, receptor, lista_mensajes)


def abrir_chat_regular(usuario, receptor, lista_mensajes):
    print(f"\nEsta es tu conversación con {receptor}\n")
    print("*"*50+"\n")
    mensajes_conversacion = list()
    for mensaje in lista_mensajes:
        if mensaje.tipo == "regular":
            if mensaje.receptor == receptor and mensaje.emisor == usuario:
                mensajes_conversacion.append(mensaje)
            elif mensaje.emisor == receptor and mensaje.receptor == usuario:
                mensajes_conversacion.append(mensaje)
    mensajes_conversacion.sort(key=ordenar_mensajes)
    for i in mensajes_conversacion:
        mensaje = "\n"
        print(f"{i.fecha} // {i.emisor}:{i.contenido}")
    print("\n" + "*"*50 + "\n")
    return escribir_mensaje(usuario, receptor, "regular")


def abrir_chat_grupal(usuario, grupo, lista_mensajes):
    print(f"\nEsta es la conversación del grupo {grupo}\n")
    print("*"*50+"\n")
    mensajes_conversacion = list()
    for mensaje in lista_mensajes:
        if mensaje.tipo == "grupo":
            if mensaje.receptor == grupo:
                mensajes_conversacion.append(mensaje)
    mensajes_conversacion.sort(key=ordenar_mensajes)
    for i in mensajes_conversacion:
        mensaje = "\n"
        print(f"{i.fecha} // {i.emisor}: {i.contenido}")
    print("\n" + "*"*50 + "\n")
    return escribir_mensaje(usuario, grupo, "grupo")


def escribir_mensaje(emisor, receptor, tipo):
    escrito = input()
    if escrito == VOLVER_FRASE:
        return menu_de_chats.menu_de_chats(emisor)
    elif escrito == ABANDONAR_FRASE:
        if tipo == "regular":
            return abrir_chat(emisor, receptor, tipo)
        elif tipo == "grupo":
            return sacar_de_grupo(emisor, receptor)
    else:
        #  Sacamos la fecha
        fecha = datetime.now()
        mes = fecha.month
        dia = fecha.day
        ano = fecha.year
        hora = fecha.hour
        minuto = fecha.minute
        segundo = fecha.second
        fecha = f"{ano}/{mes}/{dia} {hora}:{minuto}:{segundo}"
        # Creamos el mensaje con la clase
        mensaje_actual = Mensaje(tipo, emisor, receptor, fecha, escrito)
        mensaje_actual.definir_fecha()
        m = mensaje_actual
        #  Guardamos el mensaje 
        archivo_mensajes = open("mensajes.csv", "a", encoding="utf8")
        archivo_mensajes.write(f"\n{tipo},{emisor},{receptor},{fecha},{escrito}")
        archivo_mensajes.close()
        return abrir_chat(emisor, receptor, tipo)


def sacar_de_grupo(emisor, grupo):
    archivo_grupos = open("grupos.csv")
    grupos = archivo_grupos.readlines()
    archivo_grupos.close()
    for i in range(len(grupos)):
        if grupos[i] == f"{grupo},{emisor}\n":
            e = i
    grupos.pop(e)
    archivo_grupos = open("grupos.csv", "w")
    archivo_grupos.write("".join(grupos))
    archivo_grupos.close()
    print("Saliste del grupo, buena elección esos no eran tus amigos")
    return menu_de_chats.menu_de_chats(emisor)
