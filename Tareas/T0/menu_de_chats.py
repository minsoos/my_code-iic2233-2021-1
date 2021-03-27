from funciones_recurrentes import respuesta_invalida_seguir
import registro_e_inicio_de_sesion
def primer_ingreso(usuario):
    print("")
    print("*"*50 + "\n" + "*"*11 + " Has ingresado a tu chat! " + "*"*11 + "\n" + "*"*50)
    return menu_de_chats(usuario)


def menu_de_chats(usuario):
    print("\nHola ", usuario, ", ¿qué deseas hacer?")
    print("\n[1]Ver Contactos\n[2]Ver grupos\n[3]Cerrar sesión\n")
    respuesta = input()
    if respuesta == "1":
        return "menu contactos"
    elif respuesta == "2":
        return "menu grupos"
    elif respuesta == "3":
        print("\nEsperamos verte pronto!")
        return "Volver"
    else:
        print("\nRespuesta inválida")
        return menu_de_chats(usuario)


