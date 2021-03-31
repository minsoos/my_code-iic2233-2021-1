import ver_grupos
import menu_de_chats
import anadir_grupo
from funciones_recurrentes import respuesta_invalida_seguir


def menu_grupos(usuario):
    print("")
    print("*"*50 + "\n" + "*"*18 + " Menú grupos " + "*"*19 + "\n" + "*"*50)
    print("\n¿Qué desea hacer?\n")
    print("[1] Ver grupos\n[2] Añadir grupo\n[0] Volver al menú de chats\n")
    respuesta = input()
    if respuesta == "1":
        return ver_grupos.ver_grupos(usuario)
    elif respuesta == "2":
        return anadir_grupo.anadir_grupo(usuario)
    elif respuesta == "0":
        return menu_de_chats.menu_de_chats(usuario)
    else:
        desea_seguir = respuesta_invalida_seguir()
        if desea_seguir:
            return menu_grupos(usuario)
        if not desea_seguir:
            return menu_de_chats.menu_de_chats(usuario)
