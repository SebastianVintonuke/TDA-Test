def vertex_cover_min(grafo):
    if len(grafo.obtener_vertices()) == 0:
        return []
    vertices = grafo.obtener_vertices()
    return list(vertex_cover_min_rec(grafo, vertices, 0, set(vertices[:]), set(vertices[:])))


def vertex_cover_min_rec(grafo, vertices, indice, vertex_cover_actual, _vertex_cover_min):
    # Nuevo mínimo
    if len(vertex_cover_actual) < len(_vertex_cover_min):
        _vertex_cover_min = vertex_cover_actual.copy()

    # Poda, por más que quites todos los que quedan, no va a ser minimo
    n_restantes = len(vertices) - indice
    if len(vertex_cover_actual) - n_restantes > len(_vertex_cover_min):
        return _vertex_cover_min

    # Termine por esta rama
    if len(vertices) == indice:
        return _vertex_cover_min

    candidato = vertices[indice]

    if es_compatible_quitando(grafo, vertex_cover_actual, candidato):
        # Pruebo sin
        vertex_cover_actual.discard(candidato)
        resultado_con = vertex_cover_min_rec(grafo, vertices, indice + 1, vertex_cover_actual, _vertex_cover_min)
        if len(resultado_con) < len(_vertex_cover_min):
            _vertex_cover_min = resultado_con
        vertex_cover_actual.add(candidato)

    # Pruebo con
    resultado_sin = vertex_cover_min_rec(grafo, vertices, indice + 1, vertex_cover_actual, _vertex_cover_min)
    if len(resultado_sin) < len(_vertex_cover_min):
        _vertex_cover_min = resultado_sin

    return _vertex_cover_min


def es_compatible_quitando(grafo, vertex_cover_actual, candidato):
    for adyacente in grafo.adyacentes(candidato):
        if adyacente not in vertex_cover_actual:
            return False
    return True


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


if __name__ == '__main__':
    unittest.main()




