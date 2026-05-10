import pulp

# i, vertice
# Y_i, variable booleana, esta o no esta en el vertex cover
# minimizar sum(i)(Y_i), quiero la menor cantidad de vertices
# para todo vertice Y_i + sum(k)(V_k) >= 1 + M (1 - V_i)
# con k = los adyacentes del vertice i y M = k - 1
# si Y_i esta M (1 - V_i) = 0 y siempre se cumple 1 + sum(k)(V_k) >= 1
# si Y_i no esta, sum(k)(V_k) >= 1 + M, con 1 + M el numero de adyacentes
# entonces todos los adyacentes tiene que estar para cubrir esas aristas

def vertex_cover_min(grafo):
    y = []
    v = {}
    for i, v_i in enumerate(grafo.obtener_vertices()):
        v[v_i] = i
        y.append(pulp.LpVariable('Y_' + str(i), cat='Binary'))

    problem = pulp.LpProblem('vertex_cover_min', pulp.LpMinimize)

    for i, v_i in enumerate(grafo.obtener_vertices()):
        adyacentes = list(map(lambda v_k: v[v_k], grafo.adyacentes(v_i)))
        M = len(adyacentes) - 1
        problem += y[i] + pulp.LpAffineExpression([(y[k], 1) for k in adyacentes]) >= 1 + M * (1 - y[i])

    problem += pulp.lpSum(y)

    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    res = []
    for i, v_i in enumerate(grafo.obtener_vertices()):
        if pulp.value(y[i]):
            res.append(v_i)

    return res


"""
def vertex_cover_min(grafo):
    y = []
    v = {}
    for i, v_i in enumerate(grafo.obtener_vertices()):
        v[v_i] = i
        y.append(pulp.LpVariable('Y_' + str(i), cat='Binary'))

    problem = pulp.LpProblem('vertex_cover_min', pulp.LpMinimize)

    for i, v_i in enumerate(grafo.obtener_vertices()):
        for v_k in grafo.adyacentes(v_i):
            k = v[v_k]
            problem += y[i] + y[k] >= 1

    problem += pulp.lpSum(y)

    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    res = []
    for i, v_i in enumerate(grafo.obtener_vertices()):
        if pulp.value(y[i]):
            res.append(v_i)

    return res
"""



from backtracking.grafo import Grafo
import unittest

class TestVertexCoverMin(unittest.TestCase):

    def _es_vertex_cover(self, grafo, cover):
        """Función auxiliar para verificar que el conjunto cubre todas las aristas."""
        vertices = grafo.obtener_vertices()
        for v in vertices:
            for w in grafo.adyacentes(v):
                # Para cada arista (v, w), al menos uno debe estar en el cover
                if v not in cover and w not in cover:
                    return False
        return True

    def test_grafo_vacio(self):
        """Un grafo sin vértices ni aristas debe devolver un cover vacío."""
        g = Grafo(vertices_init=[])
        resultado = vertex_cover_min(g)
        self.assertEqual(len(resultado), 0)

    def test_grafo_sin_aristas(self):
        """Vértices aislados no necesitan ser cubiertos."""
        g = Grafo(vertices_init=['A', 'B', 'C'])
        resultado = vertex_cover_min(g)
        self.assertEqual(len(resultado), 0)

    def test_estrella(self):
        """
        En un grafo estrella (un centro conectado a N hojas),
        el mínimo vertex cover es solo el centro.
        """
        g = Grafo(vertices_init=['Centro', 'H1', 'H2', 'H3'])
        g.agregar_arista('Centro', 'H1')
        g.agregar_arista('Centro', 'H2')
        g.agregar_arista('Centro', 'H3')

        resultado = vertex_cover_min(g)
        self.assertEqual(len(resultado), 1)
        self.assertIn('Centro', resultado)

    def test_ciclo_tres(self):
        """En un triángulo (K3), el mínimo vertex cover es de tamaño 2."""
        g = Grafo(vertices_init=['A', 'B', 'C'])
        g.agregar_arista('A', 'B')
        g.agregar_arista('B', 'C')
        g.agregar_arista('C', 'A')

        resultado = vertex_cover_min(g)
        print(resultado)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(self._es_vertex_cover(g, resultado))

    def test_camino_lineal(self):
        """Grafo A-B-C-D. El cover mínimo es {B, C}."""
        g = Grafo(vertices_init=['A', 'B', 'C', 'D'])
        g.agregar_arista('A', 'B')
        g.agregar_arista('B', 'C')
        g.agregar_arista('C', 'D')

        resultado = vertex_cover_min(g)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(self._es_vertex_cover(g, resultado))
        # Las opciones óptimas serían {B, C} o {B, D} o {A, C},
        # pero todas tienen tamaño 2.

    def test_dos_componentes_disjuntas(self):
        """Verifica que trabaje bien con grafos no conexos."""
        g = Grafo(vertices_init=['A', 'B', 'X', 'Y'])
        g.agregar_arista('A', 'B')  # Componente 1
        g.agregar_arista('X', 'Y')  # Componente 2

        resultado = vertex_cover_min(g)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(self._es_vertex_cover(g, resultado))

    def test_ejemplo_tardos(self):
        g_tardos = Grafo(vertices_init=[1, 2, 3, 4, 5, 6, 7])
        g_tardos.agregar_arista(1, 2)
        g_tardos.agregar_arista(1, 3)
        g_tardos.agregar_arista(2, 3)
        g_tardos.agregar_arista(2, 4)
        g_tardos.agregar_arista(2, 5)
        g_tardos.agregar_arista(3, 1)
        g_tardos.agregar_arista(3, 2)
        g_tardos.agregar_arista(3, 7)
        g_tardos.agregar_arista(3, 6)
        g_tardos.agregar_arista(4, 2)
        g_tardos.agregar_arista(4, 7)
        g_tardos.agregar_arista(5, 2)
        g_tardos.agregar_arista(5, 7)
        g_tardos.agregar_arista(6, 3)
        g_tardos.agregar_arista(6, 7)
        g_tardos.agregar_arista(7, 3)
        g_tardos.agregar_arista(7, 4)
        g_tardos.agregar_arista(7, 5)
        g_tardos.agregar_arista(7, 6)
        r = vertex_cover_min(g_tardos)
        self.assertEqual([2, 3, 7], r)