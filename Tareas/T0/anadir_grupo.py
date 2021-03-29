import menu_grupos
from collections import defaultdict


def anadir_grupo(usuario):
    print("\n¿Qué grupo desea añadir?\n")
    #  revisamos archivo de grupos.csv
    grupos_archivo = open("grupos.csv")
    grupos = grupos_archivo.readlines()
    grupos_archivo.close()
    set_grupos = set()
    for i in grupos:
        i = i.split(",")
        set_grupos.add(i[0])
    #  revisamos si está el input en el archivo grupos
    nombre_grupo = input()
    if nombre_grupo in set_grupos:
        print("Este grupo ya existe :(\n")
        return menu_grupos.menu_grupos(usuario)
    else:
        print("A quiénes deseas agregar?\n")
        print("Recuerda que no puedes usar \",\" en los nombres")
        print("Además, asegúrate de que todos los miembros existan")
        print("Los miembros deben ir separados por \";\"\n")
        miembros = input()
        if "," in miembros:
            #  Revisamos si hay comas en los nombres
            print("No puede haber un nombre con coma")
            print("Además recuerda que los miembros van separados por \";\"")
            return menu_grupos.menu_grupos(usuario)
        miembros = miembros.split(";")
        miembros.append(usuario)
        miembros = list(set(miembros))
        if len(miembros)>1:
            #  Revisamos si hay más de un miembro en el input
            usuarios_archivo = open("usuarios.csv")
            usuarios = usuarios_archivo.readlines()
            usuarios_archivo.close()
            usuarios_set = set()
            for i in range(len(usuarios)):
                usuarios_set.add(usuarios[i].strip())
            existen = True
            for miembro in miembros:
                if miembro not in usuarios_set:
                    #  Revisamos si existen todos los miembros
                    existen = False
                    usuario_error = miembro
            if not existen:
                # Si no existen arrojamos error
                print(f"{usuario_error} no existe\n")
                return menu_grupos.menu_grupos(usuario)
            elif existen:
                # Agregamos al archivo grupos.csv
                grupos_archivo = open("grupos.csv", "a")
                for miembro in miembros:
                    grupos_archivo.write(f"\n{nombre_grupo},{miembro}")
                grupos_archivo.close()
                print(f"Grupo creado con éxito, ve y habla en {nombre_grupo}!")
                print("")
                return menu_grupos.menu_grupos(usuario)
        else:
            print("El grupo debe tener por lo menos dos miembros distintos")
            return menu_grupos.menu_grupos(usuario)


if __name__ == "__main__":
    anadir_grupo("lily416")