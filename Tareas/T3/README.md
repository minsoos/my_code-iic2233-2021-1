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

Qué hace cada parte del programa está indicado con comentarios en el código, pero acá se da el flujo de este de forma de poder hacer un tracking general de dónde ocurre cada cosa.

  

- La función que permite ordenar las listas del archivo ranking.txt por puntaje está en utils.py, se llama ordenar_por_puntaje()

- Aunque no se especifique repetitivamente, todas las relaciones entre ventanas distintas y backend/frontend se hacen con señales

1.  **Main.py**: Inicializa todas las ventanas, lógica y música y establece las conexiones de señales entre ellas

2.  **VentanaInicio**: Da la opción de ingresar a la ventana de preparación con un nombre de usuario ingresado en el cuadro de texto o ir a la ventana ranking.

3.  **LogicaVentanaInicio**: Si recibe la señal para iniciar partida ejecuta ```comprobar_alfanum```, que ejecuta funciones para comprobar el nombre. En caso de que esté correcto, envía una señal de aprobación a VentanaInicio, en caso contrario levanta una ventana de error. Además, si la ventana de inicio solicita entrar al ranking, abre el ranking

4.  **VentanaRanking**: Es actualizado por su lógica cada vez que se abre. Esta misma le entrega una lista con la que setea los primeros 5 lugares. En caso de que no hayan más de 5, su plantilla viene por defecto con usuario None y 0 ptos.

5.  **LogicaVentanaRanking**: Abre el archivo ranking.txt y revisa las líneas de jugadas anteriores, las ordena por orden de puntaje

6. **VentanaPreparacion**: Da la opción de elegir la dificultad mediante un QComboBox, además se puede elegir un personaje arrastrándolo al tablero. Cuando se hace, se envía una señal al backend para que haga el cambio. Con el teclado se puede mover al personaje y aumentarle la vida con un cheat. Cuando un personaje se intersecta con un edificio, envía una señal del edificio intersectado y la dificultad actual seleccionada al backend. También tiene un botón para solicitar salir a la pantalla de inicio. Por otro lado, actualiza sus datos cada vez que una señal lo solicita.

7. **VentanaMapaErrado**: Se levanta cada vez que un personaje se intersecta con un edificio que no corresponde, por una señal enviada por el backend de ventana preparación. No se muestra si no ha pasado más de TIEMPO_ENTRE_MENSAJES_DE_ERROR entre una llamada a mostrarse y otra

8. **Personajes**: La clase personaje y sus heredados modelan los personajes que controla el jugador en el juego. Estos personajes tienen un QTimer que va alternando entre las variantes 1, 2 y 3 de cada orientación cuando se solicita mover al personaje. Esto para dar la sensación de animación cuando se mueve. Además, cuando se le solicita mover, de acuerdo a su velocidad, entrega una nueva posición, que respeta obstáculos, en caso de estar en un juego, y los márgenes de este. Además, tiene una property de vida que puede ser modificada, pero no varía más allá que entre 0 y 1. Cuando esta llega a cero, envía una señal

9. **LogicaVentanaPreparacion**: Recibe la inicialización dada por la LógicaVentanaInicio, crea instancias de los personajes con los que se puede jugar. Le da una configuración de inicio a la ventana de preparación y la muestra mediante señales. Además, hace las conexiones entre la ventana y los personajes (cuando se sale de la ventana desconecta todo)
Por otro lado, cada vez que se solicita cambiar un personaje, para el QTimer del anterior, le da la información del mapa al personaje nuevo y empieza su QTimer.
Cuando recibe una señal sobre una intersección entre edificio y personaje, comprueba que sea con su personaje correspondiente. En caso positivo, cierra la ventana y abre la de juego, enviándole los datos actuales de la ventana más el personaje. En caso negativo levanta la VentanaMapaErrado
Además, es la encargada de guardar el resultado del juego en ranking.txt cuando se solicita desde la ventana de postronda o de la misma ventana de preparación cuando se solicita salir

10. **VentanaJuego**: Inicializa todo de acuerdo a parámetros fijos de las ventanas de juego y también a argumentos variables entregados por la lógica. Crea los obstáculos mediante una lista que se envía del backend. Crea el personaje revisando que no intersecte con esos obstáculos. Además realiza las conexiones, para que el objeto personaje le envíe actualizaciones de posición y se conecte a un método propio.
Con respecto al teclado, guarda las últimas 3 teclas que se presionaron, y si la tecla no es para moverse (excluyendo a la D), revisa si hay un cheat code con las últimas 3 teclas apretadas. Vale decir que cuando no se presiona una tecla de relevancia, esta misma se cambia por "z".
También hace intersects entre los objetos y el personaje, para que cuando haya uno enviar una señal al backend para que haga lo respectivo.
Cuando recibe una señal de instalar un objeto en una posición, revisa si intersecta con algo, si lo hace, pide nuevamente una señal para que el backend le dé otra posición posible hasta que haya una.
Lo demás es sólo recibir señales y mandar de acuerdo a cosas apretadas y realizar acciones, actualizaciones en tablero, etc.

11. **Gorgory**: Este personaje guarda en un deque, tuplas con el lugar x,y que se tiene que mover y cuánto tiene que esperar para moverse hacia ese lugar (estas posiciones son enviadas desde el frontend al backend y posteriormente se entregan a Gorgory, que calcula el tiempo intermedio). Con el tiempo de espera hace sleep hasta que pase el tiempo, y posteriormente se mueve hacia donde debe hacerlo

12. **CronometroSegundos**: El tiempo se mide con un cronómetro, que consiste en un QTimer que se actualiza cada 0.01 segundos, esto para poder parar el tiempo en caso de que se pause el juego

13. **LogicaVentanaJuego**: Inicializa todo de acuerdo a parametros fijos y a argumentos entregados por la lógica de la preparación cuando se solicita entrar al juego. En específico, crea un QTimer que es el encargado del tiempo de partida, un generador de objetos, que es el encargado de generar objetos de la clase Objetos cada cierto intervalo de tiempo e instanciar a Gorgory, que es el personaje malo del juego. También genera los obstáculos, enterándose de que no topen entre ellos y haya una distancia suficiente para que un personaje pueda pasar entre ellos Además, hace las conexiones entre los personajes y la ventana (los desconecta al salir de la ventana). 
Cuando recibe una señal con un objeto del generador de objeto, lo conecta, para que avise cuando caducó, y envía una señal para colocarlo en la ventana de acuerdo a una posición al azar. Cuando el objeto caduca también envía una señal para hacerlo desaparecer. También recibe señales para hacer desaparecer objetos cuando el personaje los toca, y revisa qué tipo de objeto es y qué efectos debe tener. Todo esto se hace con una lista que tiene los mismos índices en el backend que en el frontend.
La lógica también envía actualizaciones del movimiento y animación de Gorgory.
Además, maneja los distintos casos en que hay que terminar el juego, llamando a la ventana de postronda. Cuando se pausa, cambia el estado de self.pausa a True, bloqueando varios procesos, y detiene todos los QTimers del juego.
Revisa si las combinaciones del teclado sirven para cheatcodes y los ejecuta.
Además envía todas las actualizaciones a la ventana de juego

14. **VentanaJuego**: Es inicializada de acuerdo a los datos que le entrega la lógica, puede bloquear el botón de volver a la preparación si se perdió. Por lo demás, envía señales al backend de acuerdo a qué botón se apretó

15. **LogicaVentanaJuego**: De acuerdo al botón que se apretó, la lógica llama a la ventana preparación o inicio para que se abran, o bien sale del juego. Siempre suma el progreso de la partida a la ventana de preparación, pero sólo en los últimos dos casos, solicita que la ventana preparación guarde el progreso

  
  
  

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

  

  

1.  ```frontend_ventana_inicio```: Contiene a ```VentanaInicio``` y ```VentanaError```

2.  ```frontend_ventana_juego```: Contiene a ```VentanaJuego```

3.  ```frontend_ventana_preparacion```: Contiene a ```VentanaPreparacion``` y ```VentanaMapaErrado```

4.  ```frontend_ventana_ranking```: Contiene a ```VentanaRanking```

5.  ```labels_drag_drop```: Contiene a ```DragLabel``` y ```DropLabel```

6.  ```frontend_ventana_postronda```: Contiene a ```VentanaPostRonda```

7.  ```backend_ventana_inicio```: Contiene a ```LogicaVentanaInicio```

8.  ```backend_ventana_juego```: Contiene a ```LogicaVentanaJuego```

9.  ```backend_ventana_postronda```: Contiene a ```LogicaVentanaPostRonda```

10.  ```backend_ventana_preparacion```: Contiene a ```LogicaVentanaPreparacion```

11.  ```musica```: Contiene a ```Musica```

12.  ```backend_ventana_ranking```: Contiene a ```LogicaVentanaRanking```

13.  ```personajes```: Contiene a ```Personaje```, ```Homero```, ```Lisa```, ```Moe```, ```Krusty```, ```Gorgory```, ```CronometroSegundos```

11.  ```utils```: Contiene a ```Generador_de_objetos```, ```Objeto```

12.  ```parametros```: Contiene los parámetros fijos y paths usados en todo el código




## Supuestos y consideraciones adicionales :thinking:

  

Realicé los siguientes supuestos:

* Los jugadores y el servidor no se desconectan en ningún momento

* Se debe instalar la librería ```PyQt5```

* Se subió la carpeta de sprites al servidor y al usuario, ya que se sumaros sprites nuevos y los que estaban quedaron organizados de forma distinta a como se enviaron (dado la separación entre cliente y servidor)
* Se le dio un puntaje asignado a los caminos que costaban 7 baterías


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. \<https://www.programmersought.com/article/37923092494/>: Es un artículo en que enseñan a ocupar QSound

2. \<https://programtalk.com/python-examples/PyQt5.QtCore.Qt.StrongFocus/>: Enseñan a usar setFocusPolicy

3. \<https://stackoverflow.com/questions/9952553/transpaprent-qlabel/10038177>: Enseñan a poner transparencia al label, de todos modos se dejó comentado porque traía problemas

4. \<https://learndataanalysis.org/create-label-to-label-drag-and-drop-effect-pyqt5-tutorial/>: Enseñan a crear los labels drag and drop

5. \<https://doc.qt.io/qt-5/qpoint.html>: Documentación de QPoint


## Descuentos



