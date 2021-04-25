# Tarea X: Nombre de la tarea :school_satchel:

  
 ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

  
## Consideraciones generales :octocat:




  
***
<Descripción  de  lo  que  hace  y  que  **_no_**  hace  la  tarea  que  entregaron  junto

con  detalles  de  último  minuto  y  consideraciones  como  por  ejemplo  cambiar  algo

en  cierta  línea  del  código  o  comentar  una  función>

  ***

### Cosas implementadas y no implementadas :white_check_mark: :x:

No se tomarán en cuenta los ítems que no se revisan a nivel de código, pero vale recalcar que están todos hechos para considerarse completos como indica la pauta
* <Programación orientada a objetos<sub>1</sub>>: Hecha completa
* * <Los Barcos están bien modelados<sub>1.1</sub>>: Hecha completa
* * <La Mercancía está bien modelada<sub>1.2</sub>>: Hecha completa
* * <La Tripulación está bien modelada<sub>1.3</sub>>: Hecha completa
* * <Los Canales están bien modelados<sub>1.4</sub>>: Hecha completa
* * <Se utilizan clases abstractas cuando corresponde<sub>1.5</sub>>: Hecha completa
* * <Se utiliza consistentemente relaciones de agregación y composición <sub>1.6</sub>>: Hecha completa

* <Simulaciones<sub>2</sub>>: Hecha completa
* * <Se pueden crear una o más simulaciones del DCCanal<sub>2.1</sub>>: Hecha completa (No se pueden hacer simulaciones simultáneas, dicho de otra manera, la simulación acaba cuando vuelvo al menú de inicio)
* * <Se permite elegir el canal a simular<sub>2.2</sub>>: Hecha completa
* * <Se instancia correctamente el canal<sub>2.3</sub>>: Hecha completa
* * <Se instancian correctamente los barcos<sub>2.4</sub>>: Hecha completa
* * <Se instancian correctamente los tripulantes<sub>2.5</sub>>: Hecha completa
* * <Se instancian correctamente las mercancías<sub>2.6</sub>>: Hecha completa


* <Acciones<sub>3</sub>>: Hecha completa
* * <Barcos<sub>3.1</sub>>: Hecha completa
* * * <Se muestran los bacos que pueden ingresar al canal correctamente.* <sub>3.2.1</sub>>: Hecha completa
* * * <Se puede escoger un barco para ingresar al canal.<sub>3.2.2</sub>>: Hecha completa
* * * <Se implementa correctamente la acción de desplazarse<sub>3.2.3</sub>>: Hecha completa
* * * <Se implementa correctamente la probabilidad de encallar.<sub>3.2.4</sub>>: Hecha completa
* * * <Cada barco tiene sus atributos asignados correctamente según su tipo.<sub>3.2.5</sub>>: Hecha completa
* * * <Se implementa correctamente el evento especial para cada tipo de barco.<sub>3.2.6</sub>>: Hecha completa


* * <Tripulación<sub>3.2</sub>>: Hecha completa
* * * <Se implementa correctamente la habilidad especial del DCCapitán<sub>3.2.1</sub>>: Hecha completa
* * * <Se implementa correctamente la habilidad especial del DCCocinero<sub>3.2.2</sub>>: Hecha completa
* * * <Se implementa correctamente la habilidad especial del DCCarguero.<sub>3.2.3</sub>>: Hecha completa
* * * <Se asignan correctamente todos los tripulantes a sus barcos.<sub>3.2.4</sub>>: Hecha completa


* <Nombre  subitem  pauta<sub>3.1</sub>>: Hecha completa

* <Nombre  subitem  pauta<sub>2.2</sub>>: Me faltó hacer <insertar  qué  cosa  faltó>

* ...

* <Nombre  item  pauta<sub>3</sub>>: Me faltó hacer <insertar  qué  cosa  faltó>

* ...

* <Nombre  item  pauta<sub>n</sub>>: Me faltó hacer <insertar  qué  cosa  faltó>

  

## Ejecución :computer:

El módulo principal de la tarea a ejecutar es ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:

1.  ```barcos.py``` en ```T1```

2.  ```canales.py``` en  ```T1```
3. ```funciones_utiles.py``` en ```T1```
4. ```manejo_de_archivos.py``` en ```T1```
5. ```menus.py``` en ```T1```
6. ```mercancia.py``` en ```T1```
7. ```parametros.py``` en ```T1```
8. ```simular_hora.py``` en ```T1```
9. ```tripulacion.py``` en ```T1```
10. ```barcos.csv``` en ```T1```
11. ```canales.csv``` en ```T1```
12. ```mercancia.csv``` en ```T1``` 
13. ```tripulantes.csv``` en ```T1``` 
  
  

## Librerías :books:

### Librerías externas utilizadas

La lista de librerías externas que utilicé fue la siguiente:

  

1.  ```random```: ```randint()```

2.  ```currency_converter```: ```convert() / CurrencyConverter``` (debe instalarse)

3.  ```abc```: ```ABC, abstractmethod```

  

### Librerías propias

Por otro lado, los módulos que fueron creados fueron los siguientes:

  

1.  ```barcos```: Contiene a ```Barco``` y sus subclases

2.  ```canales```: Contiene a ```Canal```
3. ```mercancia```: Contiene a ```Mercancia```
4. ```tripulación```: Contiene a ```Tripulante``` y sus subclases

5.  ```funciones_utiles```: Contiene a las funciones ```ordenar_por_km()``` y ```ocurre_evento_por_probabilidad()```
6. ```manejos_de_archivos```: Hecha para <insertar  descripción  **breve**  de  lo  que  hace  o  qué  contiene>
7. ```menus```: Hecha para <insertar  descripción  **breve**  de  lo  que  hace  o  qué  contiene>
8. ```parametros```: Hecha para <insertar  descripción  **breve**  de  lo  que  hace  o  qué  contiene>
9. ```simular_hora```: Hecha para <insertar  descripción  **breve**  de  lo  que  hace  o  qué  contiene>

  

## Supuestos y consideraciones adicionales :thinking:

Los supuestos que realicé durante la tarea son los siguientes:
Asumo que en los barcos encallados no pueden ocurrir eventos

Se asume que siempre te entregarán una moneda válida

Se asume que los archivos están como los indicados

Se asume, que si simulas una hora, ya no hay vuelta atrás, por lo que si te equivocas de tecla al ingresar un barco, el programa asumirá que no quieres ingresar ningún barco

Se asume que no hay más de tres tripulantes por barco ni se repiten sus tipos en el archivo

Se asume que un barco parado no podrá encallar
  
***
1. <Descripción/consideración  1  y  justificación  del  por  qué  es  válido/a>

2. <Descripción/consideración  2  y  justificación  del  por  qué  es  válido/a>

3. ...

  ***

PD: <una  última  consideración  (de  ser  necesaria)  o  comentario  hecho  anteriormente  que  se  quiera  **recalcar**>

  
  

-------

  
  
  

**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

  

```python

class  Corrector:

  

def  __init__(self):

pass

  

# Este método coloca un 6 en las tareas que recibe

def  corregir(self, tarea):

tarea.nota =  6

return tarea

```

  

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

  

```python

def  funcion(argumento):

"""

Mi función hace X con el argumento

"""

return argumento_modificado

```

Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

  

## Referencias de código externo :book:

  

Para realizar mi tarea saqué código de:

1. \<link  de  código>: este hace \<lo  que  hace> y está implementado en el archivo <nombre.py> en las líneas <número  de  líneas> y hace <explicación  breve  de  que  hace>

  
  
  

## Descuentos

La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).