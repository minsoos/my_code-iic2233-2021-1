import registro_e_inicio_de_sesion
import menu_de_chats
import menu_contactos
import menu_grupos
#print(" "*7 + "Qué tal chaval, qué deseas hacer hoy" + " "*7)
def main():
    print("*"*50 + "\n" + "*"*11 + " Has ingresado a DCConecta2 " + "*"*11 + "\n" + "*"*50)
    ingreso = registro_e_inicio_de_sesion.funcion_interfaz_menu()
    exitoso = ingreso[0]
    usuario = ingreso[1]
    if not exitoso:
        print("revisa not exitoso línea 10 de main")
        pass
    elif exitoso:
        usuario == ingreso[1]
        accion_menu_chat = menu_de_chats.primer_ingreso(usuario)
        if accion_menu_chat == "Volver":
            return main()
        elif accion_menu_chat == "menu contactos":
            return menu_contactos.menu_contactos(usuario)
        elif accion_menu_chat == "menu grupos":
            return menu_grupos.menu_grupos(usuario)
        else:
            print("ALGO RAROOOOOOOO")

main()
#respuesta_invalida_seguir(): 
# Si el programa detecta que se ingresó este input en una conversación de grupo
# deberá sacar al usuario del grupo.
#ABANDONAR_FRASE = "\\salir"

# Si el programa detecta que se ingresó este input en cualquier conversación,
# debe volver al menú anterior.
#VOLVER_FRASE = "\\volver"
################
