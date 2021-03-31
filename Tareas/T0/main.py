import registro_e_inicio_de_sesion
import menu_de_chats


def main():
    print("*"*50 + "\n" + "*"*11 + " Has ingresado a DCConecta2 " + "*"*11 + "\n" + "*"*50)
    ingreso = registro_e_inicio_de_sesion.funcion_interfaz_menu()
    exitoso = ingreso[0]
    usuario = ingreso[1]
    if not exitoso:
        print("Igual no te queríamos con nosotros, chao\n")
        pass
    elif exitoso:
        print("")
        print("*"*50 + "\n" + "*"*11 + " Has ingresado a tu chat! " + "*"*11 + "\n" + "*"*50)
        return menu_de_chats.menu_de_chats(usuario)


if __name__ == "__main__":
    main()
