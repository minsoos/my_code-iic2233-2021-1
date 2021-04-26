import manejo_de_archivos
import menus


def acc_simular_hora(canal):
    #
    barcos_encallados = []
    for barco in canal.barcos:
        if barco.esta_encallado:
            barcos_encallados.append(barco)
    # Caso hay barcos encallados
    if len(barcos_encallados) > 0:
        barco_entrante = None
        print("\nBarcos encallados:")
        print("-"*50)
        for barco_encallado in barcos_encallados:
            print(f"Barco {barco_encallado.nombre} encallado en km {barco_encallado.km}")
        print("-"*50 + "\n")
    #
    # Caso no hay barcos encallados
    else:
        barco_entrante = elegir_barco_para_entrar(canal)
        # Si retorna None, significa ninguno
        # Si retorna 0 significa volver al menú principal
        # En cualquier otro caso, retorna el barco que se eligió
    # Ingresa un barco o no según el código de arriba
    if barco_entrante == 0:
        menus.menu_de_acciones(canal)
    elif barco_entrante != 0:
        if barco_entrante is not None:
            canal.ingresar_barco(barco_entrante)
        # Hace avanzar a los barcos del canal
        canal.avanzar_barcos()
        canal.horas_simuladas += 1
        # Vuelve al menú de acciones
        menus.menu_de_acciones(canal)


def elegir_barco_para_entrar(canal):
    # Compara barcos totales con los que están en el canal.
    # Llena una lista con los que no lo están
    barcos_totales = manejo_de_archivos.dict_barcos()
    barcos_fuera = []
    for barco in barcos_totales:
        esta_adentro = False
        for barco_adentro in canal.barcos:
            if barcos_totales[barco].nombre == barco_adentro.nombre:
                esta_adentro = True
        if not esta_adentro:
            barcos_fuera.append(barcos_totales[barco])
    # Pide elegir al usuario el barco que quiere ingresar al usuario
    print("Qué barco quieres meter?\n")
    print("[1]Ninguno")
    for i in range(len(barcos_fuera)):
        print(f"[{i+2}]{barcos_fuera[i].nombre}")
    print("[0]No simular hora y volver al menú de acciones")
    print("")
    input_usuario = input()
    # Revisa si el input es correcto, si lo es, retorna el Barco como objeto
    try:
        input_usuario = int(input_usuario)
        if input_usuario == 0:
            return 0
        if input_usuario > 0:
            if input_usuario == 1:
                print("")
                return None
            else:
                return barcos_fuera[input_usuario-2]
        else:
            print("La opción ingresada no es correcta, se vuelve al menú de acciones")
            print("La hora no se simuló")
            return 0

    except (ValueError, IndexError):
        print("La opción ingresada no es correcta, se vuelve al menú de acciones")
        print("La hora no se simuló")
        return 0
