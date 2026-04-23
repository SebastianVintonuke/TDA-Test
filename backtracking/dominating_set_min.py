def dominating_set_min(grafo):
    vertices = grafo.obtener_vertices()
    dominados = {vertice: 0 for vertice in vertices}
    return list(dominating_set_min_rec(grafo, vertices, 0, set(), dominados, set(vertices[:])))

def dominating_set_min_rec(grafo, vertices, indice, set_actual, dominados_en_set_actual, _dominating_set_min):
    # Poda ya me pase del mínimo
    if len(set_actual) >= len(_dominating_set_min):
        return _dominating_set_min

    if len(vertices) == indice:
        if es_dominating_set(dominados_en_set_actual):
            return set_actual.copy()
        else:
            return _dominating_set_min

    candidato = vertices[indice]

    # Pruebo poner
    set_actual.add(candidato)
    dominados_en_set_actual[candidato] += 1
    for adyacente in grafo.adyacentes(candidato):
        dominados_en_set_actual[adyacente] += 1

    resultado_con = dominating_set_min_rec(grafo, vertices, indice + 1, set_actual, dominados_en_set_actual, _dominating_set_min)
    if len(resultado_con) < len(_dominating_set_min):
        _dominating_set_min = resultado_con.copy()

    set_actual.remove(candidato)
    dominados_en_set_actual[candidato] -= 1
    for adyacente in grafo.adyacentes(candidato):
        dominados_en_set_actual[adyacente] -= 1

    # Pruebo no poner
    resultado_sin = dominating_set_min_rec(grafo, vertices, indice + 1, set_actual, dominados_en_set_actual, _dominating_set_min)
    if len(resultado_sin) < len(_dominating_set_min):
        _dominating_set_min = resultado_sin.copy()

    return _dominating_set_min

def es_dominating_set(dominados_en_set_actual):
    for vertice in dominados_en_set_actual:
        if dominados_en_set_actual[vertice] == 0:
            return False
    return True






from backtracking.grafo import Grafo
import unittest

class TestDominatingSetMin(unittest.TestCase):

    def _es_dominating_set(self, grafo, d_set):
        """Verifica que cada vértice del grafo esté en el set o sea vecino de uno."""
        vertices = set(grafo.obtener_vertices())
        cubiertos = set(d_set)

        for v in d_set:
            for ady in grafo.adyacentes(v):
                cubiertos.add(ady)

        return vertices == cubiertos

    def test_grafo_vacio(self):
        """Un grafo sin vértices debe devolver un set vacío."""
        g = Grafo(vertices_init=[])
        resultado = dominating_set_min(g)
        self.assertEqual(len(resultado), 0)

    def test_vertice_aislado(self):
        """Si hay un vértice sin aristas, DEBE estar en el set dominante."""
        g = Grafo(vertices_init=['A'])
        resultado = dominating_set_min(g)
        self.assertEqual(resultado, ['A'])

    def test_estrella(self):
        """En un grafo estrella, el centro domina a todos."""
        g = Grafo(vertices_init=['Centro', 'H1', 'H2', 'H3'])
        g.agregar_arista('Centro', 'H1')
        g.agregar_arista('Centro', 'H2')
        g.agregar_arista('Centro', 'H3')

        resultado = dominating_set_min(g)
        self.assertEqual(1, len(resultado))
        self.assertIn('Centro', resultado)

    def test_camino_lineal(self):
        """Grafo A-B-C-D. El set mínimo es {B, C} o {B, D}, etc. Tamaño 2."""
        g = Grafo(vertices_init=['A', 'B', 'C', 'D'])
        g.agregar_arista('A', 'B')
        g.agregar_arista('B', 'C')
        g.agregar_arista('C', 'D')

        resultado = dominating_set_min(g)
        self.assertEqual(2, len(resultado))
        self.assertTrue(self._es_dominating_set(g, resultado))

    def test_ciclo_cinco(self):
        """En un ciclo de 5 (C5), el set dominante mínimo es de tamaño 2."""
        g = Grafo(vertices_init=[1, 2, 3, 4, 5])
        g.agregar_arista(1, 2);
        g.agregar_arista(2, 3)
        g.agregar_arista(3, 4);
        g.agregar_arista(4, 5)
        g.agregar_arista(5, 1)

        resultado = dominating_set_min(g)
        self.assertEqual(2, len(resultado))
        self.assertTrue(self._es_dominating_set(g, resultado))


if __name__ == '__main__':
    unittest.main()