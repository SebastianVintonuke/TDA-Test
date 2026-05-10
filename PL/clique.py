from backtracking.grafo import Grafo
import pulp

# Cantidad de restricciones generadas en función de la cantidad de vértices $V$ y aristas $E$
# O(V)
def clique_maximo(grafo):
    V = []
    indice = {}
    for i, V_i in enumerate(grafo.obtener_vertices()):
        indice[V_i] = i
        V.append(pulp.LpVariable('V_' + str(i), cat='Binary'))

    problem = pulp.LpProblem('clique_maximo', pulp.LpMaximize)

    # Busco maximizar la cantidad de vertices en el clique
    # $max(\sum_{i} V_i)$
    problem += pulp.lpSum(V)

    # Busco que un vertice pertenezca al clique si comparte arista con otro
    # Si el vertice $i$ pertenece al clique todos los que no son adyacentes no pueden pertenecer
    # Si el vertice $i$ no pertenece al clique todos los que no son adyacentes pueden o no pertenecer
    # $\forall V_i; \quad V_i + \sum_{k} <= 1 + M(1 - V_i); \quad k \not\in adyacentes(V_i); \quad M = cant.vertices + 1$
    M = len(grafo.obtener_vertices())
    for i, V_i in enumerate(grafo.obtener_vertices()):
        problem += V[i] + pulp.LpAffineExpression([(V[indice[V_k]], 1) for V_k in not_adyacentes(grafo, V_i)]) <= 1 + M * (1 - V[i])

    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    resultado = []
    for i, V_i in enumerate(grafo.obtener_vertices()):
        if pulp.value(V[i]):
            resultado.append(V_i)

    return resultado

# O(n log n)
def not_adyacentes(grafo, vertice):
    vertices = sorted(grafo.obtener_vertices())
    adyacentes = grafo.adyacentes(vertice)
    adyacentes.append(vertice)
    adyacentes.sort(reverse=True)
    resultado = []
    i = 0
    while adyacentes:
        if vertices[i] == adyacentes[-1]:
            adyacentes.pop()
        else:
            resultado.append(vertices[i])
        i += 1
    resultado.extend(vertices[i:])
    return resultado









def cgtardos():
    g_tardos = Grafo(vertices_init=[1, 2, 3, 4, 5, 6, 7])
    g_tardos.agregar_arista(1, 2)
    g_tardos.agregar_arista(1, 3)
    g_tardos.agregar_arista(2, 3)
    g_tardos.agregar_arista(2, 4)
    g_tardos.agregar_arista(2, 5)
    g_tardos.agregar_arista(2, 7)
    g_tardos.agregar_arista(3, 1)
    g_tardos.agregar_arista(3, 2)
    g_tardos.agregar_arista(3, 7)
    g_tardos.agregar_arista(3, 6)
    g_tardos.agregar_arista(4, 2)
    g_tardos.agregar_arista(4, 5)
    g_tardos.agregar_arista(4, 7)
    g_tardos.agregar_arista(5, 2)
    g_tardos.agregar_arista(5, 7)
    g_tardos.agregar_arista(6, 3)
    g_tardos.agregar_arista(6, 7)
    g_tardos.agregar_arista(7, 3)
    g_tardos.agregar_arista(7, 4)
    g_tardos.agregar_arista(7, 5)
    g_tardos.agregar_arista(7, 6)
    return g_tardos

import unittest

class TestClique(unittest.TestCase):
    def test_1(self):
        g_tardos = cgtardos()
        print(clique_maximo(g_tardos))