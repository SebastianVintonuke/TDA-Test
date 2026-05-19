from grafo import Grafo
from collections import deque


# Modelamos la red de flujo con un grafo auxiliar igual al grafo original pero con las capacidades de cada arista modificadas a 1.
# De esta forma, al ejecutar Ford-Fulkerson los caminos de aumento no podrían compartir aristas, ya que la capacidad se satura completamente por cada camino.
# Además, notar que si pueden compartir vertice, siempre y cuando para dicho vertice el flujo de entrada sea igual al flujo de salida.
# El maximo número de caminos disjuntos será igual al flujo maximo, o al corte mínimo.
# Si se quiere reconstruir cada camino, se pueden utilizar los flujos resultantes de cada arista.
# Recorrer desde la fuente hasta el sumidero mediante las aristas intermedias sin utilizar una misma arista para multiples caminos.
# La complejidad es O(V*E^2) dado por la complejidad de FF
def disjuntos(grafo, s, t):
    red_de_flujo_valida = red_de_flujo_valida_con_pesos_1(grafo, s, t)
    flujos = flujo(red_de_flujo_valida, s, t) # O(V*E^2)
    caminos= []

    n_caminos = 0
    for v in grafo.adyacentes(s):
        n_caminos += flujos[(s, v)]

    return caminos


# Recibe un grafo y lo convierte en una red de flujo válida
def red_de_flujo_valida_con_pesos_1(grafo, s, t):
    copia_con_pesos_1 = Grafo(True, grafo.obtener_vertices())
    for v in grafo.obtener_vertices():
        for a in grafo.adyacentes(v):
            # ciclos, los saco para que la red sea válida
            if v == a:
                continue
            if v > a:
                # v y a tienen antiparalelas, pongo nodos intermedios para que la red sea válida
                if grafo.estan_unidos(a, v):
                    va = f"{v},{a}"
                    av = f"{a},{v}"
                    copia_con_pesos_1.agregar_vertice(va)
                    copia_con_pesos_1.agregar_arista(v, va, 1)
                    copia_con_pesos_1.agregar_arista(va, a, 1)
                    copia_con_pesos_1.agregar_vertice(av)
                    copia_con_pesos_1.agregar_arista(a, av, 1)
                    copia_con_pesos_1.agregar_arista(av, v, 1)
            else:
                # aristas validas
                copia_con_pesos_1.agregar_arista(v, a, 1)
    # me aseguro que s y t sean fuente y sumidero
    # no conecto las otras fuentes, total no serán caminos válidos para bfs
    super_fuente = "SUPER_S"
    super_sumidero = "SUPER_T"
    copia_con_pesos_1.agregar_vertice(super_fuente)
    copia_con_pesos_1.agregar_vertice(super_sumidero)
    # la arista con SUPER no tiene que ser el cuello de botella, el peso tien que ser igual al número de potenciales caminos
    copia_con_pesos_1.agregar_arista(super_fuente, s, len(copia_con_pesos_1.adyacentes(s)+1))
    copia_con_pesos_1.agregar_arista(t, super_sumidero, len(copia_con_pesos_1.adyacentes(t)+1))
    return copia_con_pesos_1








































def flujo(grafo, s, t):
    asignacion = {}
    for v in grafo:
        for w in grafo.adyacentes(v):
            asignacion[(v, w)] = 0
    grafo_residual = copiar(grafo)
    camino = obtener_camino(grafo_residual, s, t)
    while camino is not None:
        capacidad_residual_camino = min_peso(grafo_residual, camino)
        for i in range(1, len(camino)):
            if grafo.estan_unidos(camino[i-1], camino[i]):
                asignacion[(camino[i-1], camino[i])] += capacidad_residual_camino
            else:
                asignacion[(camino[i], camino[i-1])] -= capacidad_residual_camino
            actualizar_grafo_residual(grafo_residual, camino[i-1], camino[i], capacidad_residual_camino)
        camino = obtener_camino(grafo_residual, s, t)

    return asignacion

def actualizar_grafo_residual(grafo_residual, u, v, valor):
    peso_anterior = grafo_residual.peso_arista(u, v)
    if peso_anterior == valor:
        grafo_residual.borrar_arista(u, v)
    else:
        grafo_residual.cambiar_peso(u, v, peso_anterior - valor)
    if not grafo_residual.estan_unidos(v, u):
        grafo_residual.agregar_arista(v, u, valor)
    else:
        grafo_residual.cambiar_peso(v, u, grafo_residual.peso_arista(v, u) + valor)


def copiar(g):
    nuevo = Grafo(True, g.obtener_vertices())
    for v in g:
        for w in g.adyacentes(v):
            nuevo.agregar_arista(v, w, g.peso_arista(v, w))
    return nuevo


def obtener_camino(g, org, dst):
    padre = {org: None}
    cola = deque()
    cola.append(org)
    while len(cola) > 0:
        v = cola.popleft()
        if v == dst:
            camino = []
            while v is not None:
                camino.append(v)
                v = padre[v]
            return camino[::-1]
        for w in g.adyacentes(v):
            if w not in padre:
                padre[w] = v
                cola.append(w)
    return None


def min_peso(grafo, camino):
    cap = grafo.peso_arista(camino[0], camino[1])
    for i in range(1, len(camino) - 1):
        cap = min(cap, grafo.peso_arista(camino[i], camino[i+1]))
    return cap

import unittest
from collections import Counter

class TestCaminosDisjuntos(unittest.TestCase):
    @staticmethod
    def helper_crear_grafo(aristas, dirigido=True):
        """Crea un grafo a partir de una lista de tuplas (origen, destino, peso)."""
        vertices = set()
        for u, v, _ in aristas:
            vertices.add(u)
            vertices.add(v)

        g = Grafo(dirigido=dirigido, vertices_init=list(vertices))
        for u, v, p in aristas:
            g.agregar_arista(u, v, peso=p)
        return g

    def verificar_caminos_disjuntos(self, caminos, s, t):
        """Verifica que la lista de caminos sea válida y disjunta en aristas."""
        aristas_usadas = set()

        for camino in caminos:
            self.assertTrue(len(camino) >= 2, "El camino debe tener al menos 2 nodos.")
            self.assertEqual(camino[0], s, f"El camino no empieza en la fuente {s}.")
            self.assertEqual(camino[-1], t, f"El camino no termina en el sumidero {t}.")

            for i in range(len(camino) - 1):
                u, v = camino[i], camino[i + 1]
                arista = (u, v)
                self.assertNotIn(arista, aristas_usadas, f"Arista compartida detectada: {arista}")
                aristas_usadas.add(arista)

    def test_grafo_simple_dos_caminos(self):
        # Un diamante básico: s -> a -> t y s -> b -> t
        aristas = [('s', 'a', 1), ('a', 't', 1), ('s', 'b', 1), ('b', 't', 1)]
        grafo = self.helper_crear_grafo(aristas)
        caminos = disjuntos(grafo, 's', 't')

        self.assertEqual(len(caminos), 2)
        self.verificar_caminos_disjuntos(caminos, 's', 't')

    def test_aristas_antiparalelas(self):
        # s -> a -> b -> t y un antiparalelo b -> a que no debería afectar
        aristas = [
            ('s', 'a', 1),
            ('a', 'b', 1),
            ('b', 'a', 1),  # Antiparalela
            ('b', 't', 1)
        ]
        grafo = self.helper_crear_grafo(aristas)
        caminos = disjuntos(grafo, 's', 't')

        self.assertEqual(len(caminos), 1)
        self.verificar_caminos_disjuntos(caminos, 's', 't')

    def test_ciclos_en_grafo(self):
        # Grafo con ciclo: s -> a -> b -> c -> a -> t
        aristas = [
            ('s', 'a', 1),
            ('a', 'b', 1), ('b', 'c', 1), ('c', 'a', 1),  # Ciclo
            ('a', 't', 1)
        ]
        grafo = self.helper_crear_grafo(aristas)
        caminos = disjuntos(grafo, 's', 't')

        self.assertEqual(len(caminos), 1)
        self.verificar_caminos_disjuntos(caminos, 's', 't')

    def test_multiples_fuentes_y_sumideros(self):
        # Otras fuentes (s2) y sumideros (t2) que no son los consultados
        aristas = [
            ('s2', 'a', 1), ('s', 'a', 1),
            ('a', 'b', 1),
            ('b', 't', 1), ('b', 't2', 1)
        ]
        grafo = self.helper_crear_grafo(aristas)
        caminos = disjuntos(grafo, 's', 't')

        self.assertEqual(len(caminos), 1)
        self.verificar_caminos_disjuntos(caminos, 's', 't')

    def test_desbalance_grados(self):
        # Nodo 'x' donde Sum(aristas entrantes) > Sum(aristas salientes)
        # s -> a -> x, s -> b -> x, s -> c -> x. Pero x -> t solo tiene capacidad 1 (1 arista)
        aristas = [
            ('s', 'a', 1), ('s', 'b', 1), ('s', 'c', 1),
            ('a', 'x', 1), ('b', 'x', 1), ('c', 'x', 1),
            ('x', 't', 1)
        ]
        grafo = self.helper_crear_grafo(aristas)
        caminos = disjuntos(grafo, 's', 't')

        # El cuello de botella es x -> t, por lo que el máximo de caminos es 1.
        self.assertEqual(len(caminos), 1)
        self.verificar_caminos_disjuntos(caminos, 's', 't')

    def test_sin_camino_posible(self):
        # Dos componentes inconexos
        aristas = [('s', 'a', 1), ('b', 't', 1)]
        grafo = self.helper_crear_grafo(aristas)

        # Debe manejar grafos desconectados
        grafo.agregar_vertice('s')
        grafo.agregar_vertice('t')

        caminos = disjuntos(grafo, 's', 't')
        self.assertEqual(len(caminos), 0)

    def test_comparten_nodos_pero_no_aristas(self):
        # s -> a -> c -> t
        # s -> b -> c -> d -> t
        # Comparten el nodo 'c', pero no aristas. Es un escenario válido para disjuntos en aristas.
        aristas = [
            ('s', 'a', 1), ('a', 'c', 1), ('c', 't', 1),
            ('s', 'b', 1), ('b', 'c', 1), ('c', 'd', 1), ('d', 't', 1)
        ]
        grafo = self.helper_crear_grafo(aristas)
        caminos = disjuntos(grafo, 's', 't')

        self.assertEqual(len(caminos), 2)
        self.verificar_caminos_disjuntos(caminos, 's', 't')

    def test_no_es_red_de_flujo_valida(self):
        # Vértices sueltos, aristas que no llevan a ningún lado (callejones sin salida)
        aristas = [
            ('s', 'a', 1), ('a', 't', 1),
            ('s', 'callejon', 1), ('callejon', 'muerto', 1)
        ]
        grafo = self.helper_crear_grafo(aristas)
        grafo.agregar_vertice('huerfano')

        caminos = disjuntos(grafo, 's', 't')
        self.assertEqual(len(caminos), 1)
        self.verificar_caminos_disjuntos(caminos, 's', 't')


if __name__ == '__main__':
    unittest.main()
