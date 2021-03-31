import ver_contactos
import menu_de_chats
import anadir_contacto
from funciones_recurrentes import respuesta_invalida_seguir


def menu_contactos(usuario):
    print("")
    print("*"*50 + "\n" + "*"*17 + " MENÚ CONTACTOS " + "*"*17 + "\n" + "*"*50)
    print("\n¿Qué desea hacer?\n")
    print("[1] Ver contactos\n[2] Añadir contacto\n[0] Volver al menú de chats\n")
    respuesta = input()
    if respuesta == "1":
        return ver_contactos.ver_contactos(usuario)
    elif respuesta == "2":
        return anadir_contacto.anadir_contacto(usuario)
    elif respuesta == "0":
        return menu_de_chats.menu_de_chats(usuario)
    else:
        desea_seguir = respuesta_invalida_seguir()
        if desea_seguir:
            return menu_contactos(usuario)
        if not desea_seguir:
            return menu_de_chats.menu_de_chats(usuario)
