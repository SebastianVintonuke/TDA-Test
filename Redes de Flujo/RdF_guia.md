1. (★) Explicar para cada uno de los siguientes casos, qué modificaciones se deben aplicar sobre una red para convertirla en una red de flujo apta para la utilización del algoritmo de Ford-Fulkerson.

- a. En la red existen bucles.
- b. En la red hay ciclos de dos vértices (aristas antiparalelas).
- c. En la red hay más de una fuente.
- d. En la red hay más de un sumidero.


- a. Los bucles se pueden quitar, tanto el flujo saliente como entrante será el mismo
- b. Se debe poner 2 vertices de paso, uno por cada arista antiparalela
- c. Todas las fuentes deben conectarse a una superfuente y el flujo maximo entre sus aristas será infinito o el maximo necesario
- d. Todos los sumideros se deben conectar a un supersumidero y el flujo maximo entre sus aristas será infinito o el maximo necesario

---

2. (★★) Implementar el algoritmo de Ford-Fulkerson, asumiendo que ya está implementada una función actualizar_grafo_residual, definida como actualizar_grafo_residual(grafo_residual, u, v, valor), que recibe el grafo residual, una arista dirigida dada por los vértices u y v, y el nuevo valor del flujo a través de la arista (u,v) y actualiza el grafo residual ya teniendo en cuenta el peso anterior de la arista, y su antiparalela. Devolver un diccionario con los valores de los flujos para todas las aristas del grafo original.

```
def ford_fulkerson(grafo, s, t):
    flujos = {}
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            flujos[(v, w)] = 0
    grafo_residual = grafo.copy()
    camino = obtener_camino(grafo_residual, s, t)
    while camino:
        flujo_maximo = min(map(lambda arista: grafo_residual.peso_arista(arista[ORIGEN], arista[DESTINO]), camino))
        for arista in camino:
            flujos[arista] += flujo_maximo
            actualizar_grafo_residual(grafo_residual, arista[ORIGEN], arista[DESTINO], flujo_maximo)
        camino = obtener_camino(grafo_residual, s, t)
    return flujos
```

---

3. (★★) Dada una red y un diccionario que representa los valores de los flujos para las aristas, todos valores que respetan la restricción de cada arista, construir la red residual que refleja el estado actual de la red en función a los valores de flujo dados.

```
def red_residual(grafo, flujos):
    aristas = []
    for v in grafo.obtener_vertices():
        for a in grafo.obtener_adyacentes(v):
            aristas.append((v, a))
    _red_residual = grafo.copy()
    for arista in aristas:
        capacidad = grafo.peso_arista(arista[ORIGEN], arista[DESTINO])
        flujo = flujos[arista]
        capacidad_restante = capacidad - flujo
        if not capacidad_restante:
            _red_residual.borrar_arista(arista[ORIGEN], arista[DESTINO])
        else:
            _red_residual.cambiar_peso(arista[ORIGEN], arista[DESTINO], capacidad_restante)
        if flujo:
            _red_residual.agregar_arista(arista[DESTINO], arista[ORIGEN], flujo)
    return _red_residual
```

---

4. (★) Dada una red residual, dar un algoritmo que encuentre un camino de aumento que minimice el número de aristas utilizadas.

```
def camino_de_aumento(red_residual, s, t):
    padres = bfs(red_residual, s)
    if t not in padres:
        return None
    aristas = []
    actual = t
    while actual != s:
        aristas.append((padres[actual], actual))
        actual = padres[actual]
    aristas.reverse()
    return aristas
```

---

5. (★★) Dado un flujo máximo de un grafo, implementar un algoritmo que, si se le aumenta en una unidad la capacidad a una artista (por ejemplo, a una arista de capacidad 3 se le aumenta a 4), permita obtener el nuevo flujo máximo en tiempo lineal en vértices y aristas. Indicar y justificar la complejidad del algoritmo implementado.

```
def flujo_lineal_V3(grafo, s, t, flujos, arista):
    grafo_residual = red_residual(grafo, flujos) # O(V+E)

    hay_capacidad_restante = grafo_residual.estan_unidos(arista[ORIGEN], arista[DESTINO]) # O(1)
    if hay_capacidad_restante: # Ya sobra capacidad, aumentarla no cambia nada
        return flujos

    grafo_residual.agregar_arista(arista[ORIGEN], arista[DESTINO], 1) # La arista no tenia que existir porque no había capacidad, la creo para aumentar en 1

    camino = camino_de_aumento(grafo_residual, s, t) # O(V+E)
    if not camino: # Aumente la capacidad aca, pero el cuello de botella está en otro lado
        return flujos

    for arista_camino in camino:
        if arista_camino in flujos:
            flujos[arista_camino] += 1
        else:
            arista_opuesta = (arista_camino[DESTINO], arista_camino[ORIGEN])
            flujos[arista_opuesta] -= 1
    return flujos
```

6. (★★) Hacer un seguimiento de obtener el flujo máximo en la siguiente red de transporte, realizando las modificaciones previas que fueran necesarias. Luego, definir cuáles son los dos conjuntos del corte mínimo en dicha red.

RPL

---

7. (★★) Hacer un seguimiento de obtener el flujo máximo en la siguiente red de transporte, realizando las modificaciones previas que fueran necesarias. Luego, definir cuáles son los dos conjuntos del corte mínimo en dicha red.

RPL

---

8. (★) ¿Cuál es la relación entre el flujo máximo de una red, y un corte mínimo que separe su fuente y sumidero?

Para una red de flujo, el corte minimo tiene capacidad igual al flujo maximo.

---

9. (★★) Dado un grafo bipartito no dirigido, un match es un subconjunto de las aristas en el cual para todo vértice $v$ a lo sumo una arista del match incide en $v$ (en el match, tienen grado a lo sumo 1). Decimos que el vértice $v$ está matcheado si hay alguna arista que incida en él (sino, está unmatcheado). El matching máximo es aquel en el que tenemos la mayor cantidad de aristas (matcheamos la mayor cantidad posible). Dar una metodología para encontrar el matching máximo de un grafo, explicando en detalle cómo se modela el problema, cómo se lo resuelve y cómo se consigue el matching máximo. ¿Cuál es el orden temporal de la solución implementada?

Modelamos el grafo bipartito como una red de flujo, para esto, agregamos dos vertices, uno fuente y otro sumidero.
Conectamos cada uno de los vertices de uno de los conjuntos del grafo bipartito con el sumidero y los del otro conjunto con la fuente.
Cada nueva arista que incide en un vertice tendrá una capacidad de 1, de esta forma, el vertice solo podrá tomar un camino en el grafo original, es decir matchear con un unico vertice del otro conjunto.
De igual manera cada arista que sale de un vertice, esta vez perteneciente al conjunto opuesto, tendrá una capacidad de 1, para que análogamente solo una arista pueda matchear con él.
Luego, utilizamos el algoritmo de ford-fulkerson para encontrar el flujo maximo de la red. El algoritmo maximizará el flujo de la red, para esto usará todas las aristas que pueda, pero manteniendo las limitaciones de nuestro problema original,
dadas por la forma en que fue modelada la red, es decir, cada vertice de un conjunto solo puede estar matcheado con un vertice del otro, ya que el flujo que entra (1) en cada vertice, tiene que ser igual al flujo que sale. Esto fuerza a la red a solo poder usar una de las aristas intermedias.
Finalmente, si el flujo es igual a $V_{original}/2$, el matching es perfecto (todos machean con uno), si no, el matching maximo será inferior y se podrá obtener a partir de los flujos finales de las aristas pertenecientes al grafo original.
La complejidad del algoritmo es O($V*E^2$), complejidad de ford-fulkerson

---

10. (★★) Decimos que dos caminos son disjuntos si no comparten aristas (pueden compartir nodos). Dado un grafo dirigido y dos vértices $s$ y $t$, encontrar el máximo número de caminos disjuntos s-t en G. Dar una metodología, explicando en detalle cómo se modela el problema, cómo se lo resuelve y cómo se consigue el máximo número de caminos disjuntos. ¿Cuál es el orden temporal de la solución implementada? ¿Cómo resolverías el problema si el grafo fuera no dirigido?

Modelamos la red de flujo con un grafo auxiliar igual al grafo original pero con las capacidades de cada arista modificadas a 1.
De esta forma, al ejecutar Ford-Fulkerson los caminos de aumento no podran compartir aristas, ya que la capacidad se satura completamente por cada camino.
Además, notar que si pueden compartir vertice, siempre y cuando para dicho vertice el flujo de entrada sea igual al flujo de salida.
El maximo número de caminos disjuntos será igual al flujo maximo, o al corte mínimo.
Si se quiere reconstruir cada camino, se pueden utilizar los flujos resultantes de cada arista.
Recorrer desde la fuente hasta el sumidero mediante las aristas intermedias sin utilizar una misma arista para multiples caminos.


---

11. (★★★) Supongamos que tenemos un sistema de una facultad en el que cada alumno puede pedir hasta 10 libros de la biblioteca. La biblioteca tiene 3 copias de cada libro. Cada alumno desea pedir libros diferentes. Implementar un algoritmo que nos permita obtener la forma de asignar libros a alumnos de tal forma que la cantidad de préstamos sea máxima. Dar la metodología, explicando en detalle cómo se modela el problema, cómo se lo resuelve y cómo se consigue la máxima cantidad de préstamos. ¿Cuál es el orden temporal de la solución implementada?
