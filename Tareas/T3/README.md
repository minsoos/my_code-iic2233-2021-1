# Tarea 3: DCCópteros :school_satchel:

## Consideraciones generales :octocat:
***

- El nombre de usuario puede ser vacío, en este caso siempre se identificará como ""
- Los nombres de usuario deben ser todos diferentes, el programa se encarga de esto
- Los jugadores empiezan la partida con una cantidad de baterías al azar, restringida por los mismos límites que cuando se saca carta. No le encontraba mucho sentido a tener que sacar carta por obligación al principio del juego

***

  

### Cosas implementadas y no implementadas :white_check_mark: :x:

  

No se revisará cada subítem, pero cada uno está leído y funciona como indica la pauta, en algunos se especifican comentarios de posibles faltas.

* <networking<sub>1</sub>>: Hecha completa

* <Arquitectura cliente - servidor<sub>2</sub>>: Hecha completa
* * <Roles<sub>2.1</sub>>: Hecha completa
* * <Consistencia<sub>2.2</sub>>: Hecha completa
* * * <Se utilizan locks cuando es necesario<sub>2.2.2</sub>>: Lo de "necesario" es un poco subjetivo, pero se usa para trabajar con los diccionarios directamente relacionados con networking, ```servidor.py```
* * <Logs<sub>2.3</sub>>: Hecha completa

* <Manejo de bytes<sub>3</sub>>: Hecha completa

* <Interfaz gráfica<sub>4</sub>>: Hecha completa

* <Grafo<sub>5</sub>>: Hecha completa
* * <Funcionalidades<sub>5.3</sub>>: completo, excepto por comentario en 5.3.3
* * * <Se calcula correctamente la ruta más larga<sub>5.3.3</sub>>: Hice un dfs, pero que falla cuando no se tienen curvas simples (definición matemática: Se puede ver como un ciclo, o cuando una curva corta a otra. Se pasa por un nodo ya visitado)

* <Reglas de DCCópteros<sub>6</sub>>: Hecha completa


* <General<sub>7</sub>>: Hecha completa

* <Bonus<sub>8</sub>>: Hecho el primero
* * <GIF<sub>8.1</sub>>: Hecho completo
* * <cronometro<sub>8.2</sub>>: No hecho





## Ejecución :computer:

  

El módulo principal de la tarea a ejecutar es ```main.py``` y está en ```T3/servidor``` en el caso del servidor; y ```main.py``` y está en ```T3/usuario```. Además se debe crear los siguientes archivos y directorios adicionales:

  

1.  ```codificacion.py``` en ```T3/servidor```


2.  ```logica.py``` en ```T3/servidor```

3.  ```logica_util.py``` en ```T3/servidor```

4. ```mapa.json``` en ```T3/servidor```

5. ```parametros.json``` en ```T3/servidor```

6.  ```servidor.py``` en ```T3/servidor```

7.  ```utils.py``` en ```T3/servidor```

8.  ```Avatares``` en ```T3/servidor/sprites_servidor``` (Esta carpeta es la que se subió a ```sprites```)

9.  ```utils.py``` en ```T3/usuario```

10.  ```cliente.py``` en ```T3/usuario```

11.  ```codificacion.py``` en ```T3/usuario```

12.  ```controlador.py``` en ```T3/usuario```

13.  ```parametros.json``` en ```T3/usuario```

14.  ```ventana_espera.py``` en ```T3/usuario/ventanas```

15.  ```ventana_final.py``` en ```T3/usuario/ventanas```

16.  ```ventana_inicio``` en ```T3/usuario/ventanas```

17.  ```ventana_juego.py``` en ```T3/usuario/ventanas```

18. ```ventana_espera.ui``` en ```T3/usuario/assets```

19. ```ventana_final.ui``` en ```T3/usuario/assets```

20. ```ventana_inicio.ui``` en ```T3/usuario/assets```

21. ```ventana_juego.ui``` en ```T3/usuario/assets```

22. ```Logo``` en ```T3/usuario/sprites_usuario``` (Esta carpeta es la que se subió a ```sprites```)

23. ```Mapas``` en ```T3/usuario/sprites_usuario``` (Esta carpeta es la que se subió a ```sprites```)

24. ```pangui_celebrando``` en ```T3/usuario/sprites_usuario``` (Esta carpeta es la que se subió a ```sprites/Bonus```)

25. ```nubes.jpg``` en ```T3/usuario/sprites_usuario``` (https://peru21.pe/cheka/series/los-simpsons-y-el-error-en-su-introduccion-que-no-fue-descubierto-por-mas-de-20-anos-series-tv-fox-disney-nnda-nnlt-noticia/)

26. ```nubes_espera.jpeg``` en ```T3/usuario/sprites_usuario``` (https://static.vecteezy.com/system/resources/previews/001/221/937/non_2x/glossy-cartoon-clouds-set-vector.jpg)


***

  

## Flujo del programa :cyclone:

Acá se da el flujo del programa de forma de poder hacer un tracking general de dónde ocurre cada cosa. No pude hacerlo más detallado, hice lo que pude con el tiempo :( sorry

  

- Hay una función utils.py en el servidor y en el usuario. En ambos hay una función para cargar los parámetros desde parametros.json y para normalizar la ruta (cambiar el string por un path generado con os.path). 
- En el servidor hay una clase Nodo, que contiene todas las funciones que se hacen con ella; incluyendo los dfs para ver si se cumple el objetivo del usuario y para identidicar el camino más largod desde un nodo. También hay un camino, que es un objeto que maneja las relaciones entre los nodos. Además hay una función para recuperar la info de los nodos y caminos desde ```mapa.json```. También hay una función para contar los caminos que hay en el mapa correspondiente.
- En el usuario hay dos funciones para ordenar listas de acuerdo a ciertos parámetros, que se usan como keys en sort().

- Aunque no se especifique repetitivamente, todas las relaciones entre ventanas distintas y el controlador del usuario se hacen con señales

1.  **logica.py**: realiza toda la lógica del servidor. Apoyándose en ```logica_util.py``` (Contiene la función que se encarga de cuando un usuario intenta comprar un camino) y ```utils.py```.
Esta lógica recibe el diccionario decodificado por servidor.py (el cual se encarga del networking que se hace entre el cliente y servidor). E identifica el comando que envía el usuario. Para hacer lo que tiene configurado según este comando.
La lógica hace sus modificaciones propias e indica comandos mediante los métodos ```enviar_mensaje_a_usuario()``` y ```enviar_imagen_a_usuario()```, los cuales envían un diccionario y una imagen, respectivamente, a servidor, quien lo codifica y lo envía a usuario.
El código está separado por secciones mediante ```# --------------```.
Se hacen "logs" con ciertos hitos en el código

2.  **controlador.py**: Recibe un comando desde el servidor de la misma manera que la lógica del servidor y lo ejecuta. Este controlador además alberga las instanciaciones de las ventanas. Aquí, se conectan las señales de estas y hacias ellas


  
  

## Librerías :books:


### Librerías externas utilizadas

  

La lista de librerías externas que utilicé fue la siguiente:

  

  

1.  ```PyQt5```: ```QtCore, QtGui, uic, QtWidgets, ``` (debe instalarse)

  

2.  ```random```: ```randint(), choice()```

  
3. ```socket```

4.  ```threading```

5.  ```json```

6.  ```collections```: ```deque```

  

  

### Librerías propias

  

Por otro lado, los módulos que fueron creados fueron los siguientes:

  

  

1.  ```servidor/logica```: Contiene a ```Logica```

2.  ```servidor/servidor```: Contiene a ```Servidor```

3.  ```usuario/ventana_espera```: Contiene a ```VentanaEspera```

4.  ```usuario/ventana_final```: Contiene a ```VentanaFinal```

5.  ```usuario/ventana_inicio```: Contiene a ```VentanaInicio```

6.  ```usuario/ventana_juego```: Contiene a ```VentanaJuego```

7.  ```usuario/cliente```: Contiene a ```Cliente```

8.  ```usuario/controlador```: Contiene a ```Controlador```


## Supuestos y consideraciones adicionales :thinking:

  

Realicé los siguientes supuestos:

* Los jugadores y el servidor no se desconectan en ningún momento

* Se debe instalar la librería ```PyQt5```

* Se subió la carpeta de sprites al servidor y al usuario, ya que se sumaron sprites nuevos y los que estaban quedaron organizados de forma distinta a como se enviaron (dado la separación entre cliente y servidor)

* Se le dio un puntaje asignado a los caminos que costaban 7 baterías


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. \<https://pythonpyqt.com/pyqt-gif/>: Enseñan a setear gifs

2. \<https://stackoverflow.com/questions/59866185/how-to-draw-with-qpainter-on-top-of-already-placed-qlabel-or-qpixmap>: Enseña a dibujar rectas sobre un label


## Descuentos

Hardcoding de el puerto y la dirección ip en servidor y usuario


