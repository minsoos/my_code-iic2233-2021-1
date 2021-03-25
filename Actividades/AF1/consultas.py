import cargar
from collections import defaultdict
platos = cargar.cargar_platos()
print(platos)
def platos_por_categoria(platos):
    diccionario = defaultdict(list)
    for i in platos:
        diccionario[platos[i].categoria].append(platos[i].n)
    return diccionario
    ##############
    categorias = set()
    #for i in platos:
       # categorias.add(i.categoria)
    #for i in categorias:
      #  for e in range(len(platos)):



# Retorna los platos que no incluyan los ingredientes descartados
def descartar_platos(ingredientes_descartados, platos):
    for i in platos:
        tiene_ingrediente_descartado = False
        for e in ingredientes_descartados:
            for h in platos[i].ingredientes:
                if e == h:
                    tiene_ingrediente_descartado = True
        if tiene_ingrediente_descartado == True:
            del platos[platos[i].n]
    return platos


# Recibe un plato, comprueba si hay ingredientes suficientes y los descuenta
def ordenar_plato(plato, ingredientes):
    # COMPLETAR ESTA FUNCIÖN
    pass


# Recibe una lista de platos y retorna el resumen de esa orden
def resumen_orden(lista_platos):
    # COMPLETAR ESTA FUNCIÖN
    pass


if __name__ == "__main__":
    # ================== PUEDES PROBAR TUS FUNCIONES AQUÍ =====================
    print(" PRUEBA CONSULTAS ".center(80, "="))
    platos_por_categoria(platos)
    descartar_platos(ingredientes_descartados, platos)
