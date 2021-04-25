import manejo_de_archivos
import menus


def acc_simular_hora(canal):
    #
    barcos_encallados = []
    for barco in canal.barcos:
        if barco.esta_encallado:
            barcos_encallados.append(barco)
    if len(barcos_encallados) > 0:
        barco_entrante = None
        print("\nBarcos encallados:")
        print("-"*50)
        for barco_encallado in barcos_encallados:
            print(f"Barco {barco_encallado.nombre} encallado en km {barco_encallado.km}")
        print("-"*50 + "\n")
    else:
        barco_entrante = elegir_barco_para_entrar(canal)
    if barco_entrante is not None:
        canal.ingresar_barco(barco_entrante)
    canal.avanzar_barcos()
    canal.horas_simuladas += 1
    menus.menu_de_acciones(canal)


def elegir_barco_para_entrar(canal):
    barcos_totales = manejo_de_archivos.dict_barcos()
    barcos_fuera = []
    for barco in barcos_totales:
        esta_adentro = False
        for barco_adentro in canal.barcos:
            if barcos_totales[barco].nombre == barco_adentro.nombre:
                esta_adentro = True
        if not esta_adentro:
            barcos_fuera.append(barcos_totales[barco])
    print("Qué barco quieres meter?\n")
    print("[1]Ninguno")
    for i in range(len(barcos_fuera)):
        print(f"[{i+2}]{barcos_fuera[i].nombre}")
    print("")
    input_usuario = input()
    try:
        input_usuario = int(input_usuario)
        if input_usuario > 0:
            if input_usuario == 1:
                return None
            else:
                return barcos_fuera[input_usuario-2]
        else:
            print("La opción ingresada no es correcta, no se ingresará ningún barco")

    except (ValueError, IndexError):
        print("La opción ingresada no es correcta, no se ingresará ningún barco")
        return None
