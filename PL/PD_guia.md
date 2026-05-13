### Cheatsheet

$Or$ de $n$ variables: $Y_{or} \le \sum_{i} Y_i \le n * Y_{or}$

$And$ de $n$ variables: $n * Y_{and} \le \sum_{i} Y_i \le (n - 1) + Y_{and}$

$Not$ de 1 variable: (1 - $Y_i$)

Secuencia

$P_i$ numero de secuencia

$P_i - P_j + n * Y_{i,j} \le n - 1$

---

### 1. (★) Implementar un modelo de programación lineal que resuelva el Problema de la Mochila de valor máximo (ejercicio 7 de PD).

- $e_i$, llevo o no llevo el elemento $i$ (variable binaria)
- $p_i$, peso del elemento $i$ (constante)
- $v_i$, valor del elemento $i$ (constante)
- $W$, peso máximo (constante) 

Busco maximizar el valor:

$\max(\sum_{i} e_i * v_i)$

Busco no pasarme del peso:

$\sum_{i} e_i * p_i \le W $

---

### 2. (★) Implementar un modelo de programación lineal que resuelva el problema de Juan El Vago (ejercicio 4 de PD).

- $d_i$ trabajo o no trabajo el dia $i$ (variable booleana)
- $v_i$ valor de trabajar el dia $i$ (constante)

Busco maximizar la ganancia:

$\max(\sum_{i} d_i * v_i)$

Busco no trabajar dos dias seguidos:

$d_i + \sum_{k} d_k <= 1 + M(1 - d_i)$

$d_k \in adyacentes(d_i) \quad y \quad M = 3$

Otra alternativa:

$\forall i \in (0,n-2); \quad d_i + d_{i+1} \le 1$

---

### 3. (★) Implementar un modelo de programación lineal que resuelva el problema de Vertex Cover mínimo (ejercicio 13 de BT).

- $v_i$ incluyo o no incluyo el vertice $i$ (variable booleana)

Busco minimizar el numero de vertices incluidos

$\min(\sum_{i} v_i)$

Busco que si un vertice no está, todos sus adyacentes tienen que estar para cubrir todas las aristas,
si el vertice esta, los adyacentes pueden o no estar

$\forall v_i \quad v_i + \sum_{k} v_k >= 1 + M(1 - v_i); \quad v_k \in adyacente(v_i); \quad M = k - 1$


---

### 4. (★) Implementar un modelo de programación lineal que resuelva el problema de Dominating Set mínimo (ejercicio 14 de BT).

- $v_i$ incluyo o no incluyo el vertice $i$ (variable booleana)

Busco minimizar el número de vertices incluidos

$\min(\sum_{i} v_i)$

Busco que si el vertice no está, algún adyacente tiene que estar para cubrirlo,
si esta, los adyacentes pueden o no estar

$\forall v_i; \quad v_i + \sum_{k} v_k >= 1; \quad v_k \in adyacentes(v_i)$

---

### 5. (★) Implementar un modelo de programación lineal que resuelva el problema de 3-SAT mínimo: que encuentre una solución que satisfaga, utlizando la menor cantidad de variables en true posible.

- $v_i$ la variables $i$ es True o False (variable booleana)
- $c_j$ la condición $j$ se cumple o no (variable booleana)

Busco minimizar el número de variables en True

$\min(\sum_{i} v_i)$

Busco que se cumplan todas las condiciones

$\forall c_j; \quad c_j >= 1$

Busco que cada condición sea un $or$ de 3 variables

como sumatoria:

$c_j \le \sum_{k} v_k \le n * c_j; \quad v_k \in variables(c_j); \quad k \in (1, 2, 3); \quad n = 3 $

u otra opción directamente:

$c_j \le v_{k1} + v_{k2} + v_{k3} \le n * c_j; \quad v_k \in variables(c_j); \quad k \in (1, 2, 3); \quad n = 3 $

Dentro de una condición una variable podría ser negada? "A and B and NOT C"
En ese caso:

$c_j \le \sum_{kp} v_{kp} + \sum_{kn} (1 - v_{kn}) \le n * c_j; \quad v_{kp} \in variablesPositivas(c_j); \quad v_{kn} \in variablesNegativas(c_j); \quad v_{kp} + v_{kn} = 3 = n$


---

### 6. (★★★) Implementar un modelo de programación lineal que resuelva el problema de Independent Set Máximo.

- $v_i$ incluyo o no incluyo el vertice $i$ (variable booleana)

Busco maximizar el número de vertices

$\max(\sum_{i} v_i)$

Busco que si un vertice está incluido, sus adyacentes no pueden estar incluidos,
si no está incluido, sus adyacentes pueden o no estar

$\forall v_i; \quad v_i + \sum_{k} v_k \le 1 + M(1 - v_i); \quad k \in adyacentes(v_i); \quad M = cant.vertices + 1$

---

### 7. (★★) Implementar un modelo de programación lineal que determine la cantidad mínima de colores a utilizar para poder pintar a un grafo de colores, de tal forma que ningún adyacente comparta color entre sí.

$V_{i,j}$ el vertice $i$ tiene el color $j$ (variable booleana)
$U_j$ se usa el color $j$ (variable booleana)

Busco saber que colores se usan ($or$ de los vertices con ese color)

$\forall U_j; \quad U_j \le \sum_{i} V_{i,j} \le n * U_j; \quad n = cant.vertices$

Busco minimizar el número de colores usados

$min(\sum_{j}) U_j$

Busco que cada vertice solo tenga un color

$\forall V_{i,j}; \quad \sum_{j} V_{i,j} = 1$

Busco que los vertices adyacentes no compartan color
Si el vertice $i$ es color $j$ la suma de sus adyacentes en $j$ tiene que ser 0
si el vertice $i$ no es color $j$ la suma de sus adyacentes en $j$ puede ser cualquier cosa

$\forall V_{i,j}; \quad V_{i,j} + \sum_{k} V_{k,j} \le 1 + M(1 - V_{i,j}); \quad k \in adyacentes(V_{i,j}); \quad M = cant.vertices + 1 $

---

### 8. (★★) Implementar un modelo de programación lineal que permita determinar el clique de tamaño máximo dentro de un grafo. Indicar la cantidad de restricciones generadas en función de la cantidad de vértices y aristas (podés usar notación O para esto, no es importante el número exacto).

- $V_i$ el vertice $i$ pertenece al clique $j$ (variable booleana)

Busco maximizar la cantidad de vertices en el clique

$max(\sum_{i} V_i)$

Busco que un vertice pertenezca al clique si comparte arista con otro\
Si el vertice $i$ pertenece al clique todos los que no son adyacentes no pueden pertenecer\
Si el vertice $i$ no pertenece al clique todos los que no son adyacentes pueden o no pertenecer

$\forall V_i; \quad V_i + \sum_{k} <= 1 + M(1 - V_i); \quad k \not\in adyacentes(V_i); \quad M = cant.vertices + 1$

---

### 9. (★★★) Osvaldo es un empleado de una inescrupulosa empresa inmobiliaria, y está buscando un ascenso. Está viendo cómo se predice que evolucionará el precio de un inmueble (el cual no poseen, pero pueden comprar). Tiene la información de estas predicciones en el arreglo pp, para todo día i=1,2,...,ni=1,2,...,n. Osvaldo quiere determinar un día jj en el cuál comprar la casa, y un día kk en el cual venderla (k>jk>j), suponiendo que eso sucederá sin lugar a dudas. El objetivo, por supuesto, es el de maximizar la ganancia dada por p[k]−p[j]p[k]−p[j].
### Implementar un modelo de programación lineal que determine el día de compra y el día de venta del inmueble. Indicar la cantidad de restricciones implementadas para esto.

- $V_i$ valor del inmueble el día $i$ (constante)
- $J_i$ si se compra el día $i$ (variable booleana)
- $K_i$ si se vende el día $i$ (variable booleana)
- $P_i$ numero de secuencia del dia $i$ (constante)

Busco que solo se pueda comprar un día

$\sum_{i} J_i = 1$

Busco que solo se pueda vender un día

$\sum_{i} K_i = 1$

Busco maximizar la ganancia, es decir la diferencia entre el dia que se compra y el dia que se vende

$max(sum_{i} K_i * V_i - sum_{i} J_i * V_i)$

Busco que el número de secuencia del día que se compra sea anterior al del dia que se vende

$\sum_{i} J_i * P_i <= \sum_{i} K_i * P_i$

### 10. (★★★★) Dado un arreglo de enteros ordenado, un elemento y un valor entero k, se quiere encuentrar los k valores del arreglo más cercanos al elemento en cuestión (que bien podría estar en el arreglo, o no). Realizar un modelo de programación lineal que resuelva este problema. OJO nos interesa que sean cercanos al elemento, y eso se ve con el valor absoluto de la diferencia, y el operador módulo no es un operador lineal. Si se incluye el operador módulo como parte del Modelo, el ejercicio estará Mal. Resolver de tal manera que el modelo sea el que resuelva estas diferencias. Indicar la cantidad de restricciones definidas.

- $Y_i$ Si incluyo el elemento $i$ (variable booleana)
- $k$ Cantidad de valores a encontrar (constante entera)
- $D_{i}$ Distancia desde el elemento $i$ hasta el elemento dado (constante entera)

Busco no incluir mas de $k$ elementos

$\sum_{i} Y_i \le k$

Por un lado, busco maximizar la cantidad de elementos incluidos

$\max(\sum_{i} Y_i)$

Por otro lado, busco minimizar la suma de las distancias\
(si los valores son los más cercanos, entonces la suma de las distancias va a ser la mínima)

$\min( \sum_{i} Y_i * D_i )$

Busco combinar ambos requerimientos en una unica expresión a optimizar\
Busco minimizar la expresión $A-B$ donde $A$ es la sumatoria de las distancias
y $B$ es la sumatoria de los elementos seleccionados por un elemento muy grande.\
De esta forma conviene incluir tantos elementos como $k$ me permita de modo de maximizar el sustraendo $B$
y elegir las distancias más pequeñas de modo de minimizar el minuendo $A$, minimizando la diferencia $A-B$

$\min( \sum_{i} Y_i * D_i - \sum_{i} Y_i * M); \quad M = max(D_i) + 1$

---

## (★★) Se está formando una nueva comisión de actividades culturales de un pueblo. Cada habitante es miembro de 0 o más clubes, y de exactamente 1 partido político. Cada uno de los nn clubes debe nombrar a un representante ante la nueva comisión de actividades culturales, con las siguientes restricciones: cada partido político no puede tener más de n22n​ simpatizantes en la comisión, y además queremos minimizar la cantidad simpatizantes a un mismo partido político; cada persona puede representar a solo un club, cada club debe estar representado por un miembro.
## Implementar un modelo de programación lineal que dada la información de los habitantes (a qué clubes son miembros, a qué partido pertenecen), nos permita obtener los representantes válidos, que además minimicen la cantidad de simpatizantes a un mismo partido político. Indicar la cantidad de inecuaciones definidas en el modelo.

- $n$ cantidad de clubes
- $C_{i,c}$ La persona $i$ pertenece al club $c$ (constante booleana)
- $P_{i,p}$ La persona $i$ pertenece al partido politico $p$ (constante booleana)
- $R_{i,c}$ La persona $i$ representa al club $c$ en la comisión (variable booleana)
- $RP_{i,p}$ La persona $i$ es del partido politico $p$ y es representante en la comisión (variable booleana)
- $RPIJ_{i,j,p}$ La persona $i$ es representante en la comisión, la persona $j$ es representante en la comisión y ambos son del partido politico $p$ (variable booleana)

La persona $i$ es del partido politico $p$ y es representante en la comisión:

# $\forall (i,p); RP_{i,p} = P_{i,p} * \sum_{c} R_{i,c}$

La persona $i$ es representante en la comisión, la persona $j$ es representante en la comisión y ambos son del partido politico $p$ (variable booleana):

# $\forall (i,j,p); \quad 2 * RPIJ_{i,j,p} \le RP_{i,p} + RP_{j,p} \le 1 + RPIJ_{i,j,p}$

Cada partido político no puede tener más de $\frac{n}{2}$ simpatizantes en la comisión:

# $\forall p; \quad \sum_{i} RP_{i,p} \le \frac{n}{2}$

Queremos minimizar la cantidad simpatizantes a un mismo partido político:

# $\min( \sum_{i} \sum_{j} \sum_{p} RPIJ_{i,j,p} )$

Cada persona puede representar a solo un club:

# $\forall i; \quad \sum_{c} R_{i,c} \le 1$

Cada club debe estar representado por un miembro:

# $\forall c; \quad \sum_{i} R_{i,c} = 1$

Si $i$ es representante esta en el club\
Si $i$ no es representante puede o no estar en el club

# $\forall (i,c); \quad   R_{i,c} + (1 - C_{i,c}) \le 1 + M * (1 - R_{i,c})$

Otra opción:

# $\forall (i,c); \quad R_{i,c} \le C_{i,c}$

El modelo está formado por $i*p + i^2*p + p + i + n + i*n$ inecuaciones,\
es decir $p*(i^2+i+1) + n*(i+1) + i$\
Si solo incluyo inecuaciones $i^2*p + p + i + i*n$,\
es decir $i(i*p + p + 1 + n)$

---

## (★★) El 2-Partition Problem como problema de optimización se describe tal que: Dado un conjunto de $n$ números positivos $T= \lbrace T_1, T_2, \dots, T_n \rbrace$, se particionan los números en dos subconjuntos $S_1$ y $S_2$ (con intersección vacía y unión = T) de forma de minimizar la sumatoria de cualquiera de los subconjuntos ($\min \max (S_1, S_2)$).

## Implementar un modelo de programación lineal que dados los valores de los $T_i$ nos permita obtener la asignación óptima para $S_1$ y $S_2$. Indicar la cantidad de inecuaciones definidas en el modelo.

- $n$ Cantidad de números (constante entera)
- $T_i$ El valor de el número $i$ (constante entera)
- $S1_i$ El número $i$ pertenece al subconjunto $S_1$ (variable booleana)
- $S2_i$ El número $i$ pertenece al subconjunto $S_2$ (variable booleana)

Busco que cada $i$ tenga que estar en un y solo un subconjunto

# $\forall i; \quad S1_i + S2_i = 1$

Busco que $S1$ sea mas grande o igual a $S2$

# $\sum_{i} S1_i *T_i \ge \sum_{i} S2_i * T_i$

Busco minimizar la sumatoria del más grande

# $\min( \sum_{i} S1_i * T_i )$

El modelo está formado por $i + 2$ inecuaciones

---

### 10. (★★★★) Dado un arreglo de enteros ordenado, un elemento y un valor entero k, se quiere encuentrar los k valores del arreglo más cercanos al elemento en cuestión (que bien podría estar en el arreglo, o no). Realizar un modelo de programación lineal que resuelva este problema. OJO nos interesa que sean cercanos al elemento, y eso se ve con el valor absoluto de la diferencia, y el operador módulo no es un operador lineal. Si se incluye el operador módulo como parte del Modelo, el ejercicio estará Mal. Resolver de tal manera que el modelo sea el que resuelva estas diferencias. Indicar la cantidad de restricciones definidas.

- $E$ Valor del elemento dado (constante)
- $K$ Cantidad de valores a encontrar (constante entera)
- $V_i$ Valor del elemento $i$ (constantes enteras)
- $Y_i$ Si incluyo el elemento $i$ (variables booleanas)

- $D_i$ Distancia del elemento $i$ al elemento $E$ (variable entera)
- $auxY_iD_i$ Si el elemento $i$ se incluye la distancia a $E$, si no $0$ (variable entera)


- $A_i$ El elemento $i$ esta antes que el elemento $E$ (constante booleana)
- $D_i$ Distancia del elemento $i$ al elemento $E$ (variable entera)

# $\forall i; \quad D_i >= 0$
# $\forall i; \quad D_i = P_i - P_E; \quad \not A_i$
# $\forall i; \quad D_i = P_E - P_i; \quad A_i$




Busco solo incluir $K$ valores:

### $\sum_{Y_i} \le K$

Busco que lo valores incluidos sean los más cercanos

### $\min( \sum_{i} auxY_iD_i )$

Construyo $auxY_iD_i$ la cual es $Y_i * D_i$

### $\forall i; \quad auxY_iD_i >= 0$
### $\forall i; \quad auxY_iD_i <= D_i$
### $\forall i; \quad auxY_iD_i <= M * Y_i; \quad M = max(D_i)$
### $\forall i; \quad auxY_iD_i >= D_i - M * (1 - Y_i)$














































