from funciones_recurrentes import respuesta_invalida_seguir
import registro_e_inicio_de_sesion
import main
import menu_contactos
import menu_grupos


def interfaz_menu_de_chats(usuario):
    print("")
    print("*"*50 + "\n" + "*"*17 + " MENÚ DE CHATS " + "*"*18 + "\n" + "*"*50)
    print("\nHola", f"{usuario}, ¿qué deseas hacer?")
    print("\n[1]Menú Contactos\n[2]Menú grupos\n[0]Cerrar sesión\n")
    respuesta = input()
    if respuesta == "1":
        return "menu contactos"
    elif respuesta == "2":
        return "menu grupos"
    elif respuesta == "0":
        print("\nEsperamos verte pronto!\n")
        return "Volver"
    else:
        print("\nRespuesta inválida")
        return menu_de_chats(usuario)


def menu_de_chats(usuario):
    accion_menu_chat = interfaz_menu_de_chats(usuario)
    if accion_menu_chat == "Volver":
        return main.main()
    elif accion_menu_chat == "menu contactos":
        return menu_contactos.menu_contactos(usuario)
    elif accion_menu_chat == "menu grupos":
        return menu_grupos.menu_grupos(usuario)
    else:
        pass
