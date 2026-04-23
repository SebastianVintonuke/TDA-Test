from backtracking.grafo import Grafo

def independent_set(grafo):
    vertices = grafo.obtener_vertices()
    return independent_set_rec(grafo, vertices, [], [])


def independent_set_rec(grafo, vertices, independent_set_actual, independent_set_maximo):
    if len(independent_set_actual) > len(independent_set_maximo):
        mejor_resultado = independent_set_actual
    else:
        mejor_resultado = independent_set_maximo

    if not vertices:
        return mejor_resultado

    # Si ya no llego corto
    if (len(vertices) + len(independent_set_actual)) <= len(independent_set_maximo):
        return independent_set_maximo

    candidato = vertices.pop()
    if es_compatible(grafo, independent_set_actual, candidato):
        # Pruebo poner
        independent_set_actual.append(candidato)
        resultado_con = independent_set_rec(grafo, vertices, independent_set_actual, mejor_resultado)[:]
        # Restauro el estado
        independent_set_actual.remove(candidato)

        if len(resultado_con) > len(mejor_resultado):
            mejor_resultado = resultado_con
    # Pruebo no poner
    resultado_sin = independent_set_rec(grafo, vertices, independent_set_actual, mejor_resultado)[:]
    vertices.append(candidato)

    if len(resultado_sin) > len(mejor_resultado):
        mejor_resultado = resultado_sin

    return mejor_resultado


def es_compatible(grafo, independent_set_actual, candidato):
    for vertice in independent_set_actual:
        if grafo.estan_unidos(vertice, candidato):
            return False
    return True


# O(n^2)
def independent_set_greedy_aproximado(grafo):
    candidatos = sorted(grafo.obtener_vertices(), key=lambda v: len(grafo.adyacentes(v)))
    independent_set_aproximado = []
    for candidato in candidatos:
        if es_compatible(grafo, independent_set_aproximado, candidato):
            independent_set_aproximado.append(candidato)
    return independent_set_aproximado



"""

def independent_set(grafo):
    vertices = grafo.obtener_vertices()
    return independent_set_rec(grafo, vertices, [], [])

def independent_set_rec(grafo, vertices, independent_set_actual, independent_set_maximo):
    if not vertices:
        return independent_set_actual
    
    if len(vertices) + len(independent_set_actual) < len(independent_set_maximo):
        return independent_set_maximo

    candidato = vertices.pop()
    adyacentes = set(grafo.adyacentes(candidato))
    compatibles = [v for v in vertices if v not in adyacentes]

    # Pruebo poner
    independent_set_actual.append(candidato)
    resultado_con = independent_set_rec(grafo, compatibles, independent_set_actual, independent_set_maximo)[:]
    independent_set_actual.remove(candidato)

    # Pruebo no poner
    resultado_sin = independent_set_rec(grafo, vertices, independent_set_actual, independent_set_maximo)[:]
    vertices.append(candidato)

    return resultado_con if len(resultado_con) >= len(resultado_sin) else resultado_sin
"""

import time
import random
import unittest

random.seed(12)

def generar_grafo_aleatorio(n_vertices, prob_arista):
    """
    Genera un grafo con 'n_vertices'.
    La existencia de cada arista posible se evalúa contra 'prob_arista'.
    """
    g = Grafo(dirigido=False)
    for i in range(n_vertices):
        g.agregar_vertice(i)

    for i in range(n_vertices):
        for j in range(i + 1, n_vertices):
            if random.random() < prob_arista:
                g.agregar_arista(i, j)
    return g

class TestIndependentSet(unittest.TestCase):
    def es_conjunto_independiente(self, grafo, resultado):
        """Función auxiliar para validar las reglas del conjunto independiente."""
        vertices = set(resultado)
        for v in vertices:
            for ady in grafo.adyacentes(v):
                if ady in vertices:
                    return False  # Se encontró una arista entre dos nodos del conjunto
        return True

    def test_grafo_vacio(self):
        g = Grafo(dirigido=False)
        resultado = independent_set(g)
        self.assertEqual(resultado, [], "Un grafo vacío debería devolver una lista vacía.")

    def test_un_solo_vertice(self):
        g = Grafo(dirigido=False)
        g.agregar_vertice("A")
        resultado = independent_set(g)
        self.assertEqual(resultado, ["A"], "Un solo vértice es siempre un conjunto independiente.")

    def test_grafo_completo_K3(self):
        # En un grafo completo, el conjunto independiente máximo es de tamaño 1
        g = Grafo(dirigido=False)
        for v in ["A", "B", "C"]: g.agregar_vertice(v)
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "C")
        g.agregar_arista("A", "C")

        resultado = independent_set(g)
        self.assertEqual(len(resultado), 1)
        self.assertTrue(self.es_conjunto_independiente(g, resultado))

    def test_camino_lineal(self):
        # A - B - C - D. Solución máxima: {A, C} o {B, D} (tamaño 2)
        g = Grafo(dirigido=False)
        vertices = ["A", "B", "C", "D"]
        for v in vertices: g.agregar_vertice(v)
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "C")
        g.agregar_arista("C", "D")

        resultado = independent_set(g)
        self.assertTrue(self.es_conjunto_independiente(g, resultado))
        self.assertEqual(len(resultado), 2, "Para un camino de 4, el conjunto máximo es 2.")

    def test_grafo_disconexo(self):
        # A-B  C-D. El conjunto independiente debería tomar elementos de ambos componentes.
        g = Grafo(dirigido=False)
        for v in ["A", "B", "C", "D"]: g.agregar_vertice(v)
        g.agregar_arista("A", "B")
        g.agregar_arista("C", "D")

        resultado = independent_set(g)
        self.assertTrue(self.es_conjunto_independiente(g, resultado))
        self.assertEqual(len(resultado), 2)

    def test_tardos(self):
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
        print(independent_set(g_tardos))

    def ejecutar_prueba_volumen(self, n_vertices, prob_arista):
        grafo = generar_grafo_aleatorio(n_vertices, prob_arista)

        inicio = time.time()
        resultado = independent_set(grafo)
        fin = time.time()

        tiempo_ejecucion = fin - inicio
        print(f"Vértices: {n_vertices:<3} | Prob. Arista: {prob_arista:<4.2f} | "
              f"Tamaño Set: {len(resultado):<2} | Tiempo: {tiempo_ejecucion:.5f}s")

        self.assertTrue(self.es_conjunto_independiente(grafo, resultado),
                        "El resultado devuelto en el test de volumen no es un conjunto independiente válido.")

    def test_volumen_n10(self):
        print("\n--- Volumen: 10 Vértices ---")
        self.ejecutar_prueba_volumen(10, 0.2)
        self.ejecutar_prueba_volumen(10, 0.5)
        self.ejecutar_prueba_volumen(10, 0.8)

    def test_volumen_n20(self):
        print("\n--- Volumen: 20 Vértices ---")
        self.ejecutar_prueba_volumen(20, 0.2)
        self.ejecutar_prueba_volumen(20, 0.5)
        self.ejecutar_prueba_volumen(20, 0.8)

    def test_volumen_n30_disperso(self):
        print("\n--- Volumen: 30 Vértices (Disperso) ---")
        # Para N=30, densidades altas pueden tardar significativamente debido a la complejidad exponencial.
        self.ejecutar_prueba_volumen(30, 0.1)
        self.ejecutar_prueba_volumen(30, 0.2)

    def test_volumen_n40_muy_disperso(self):
        print("\n--- Volumen: 40 Vértices (Muy Disperso) ---")
        self.ejecutar_prueba_volumen(40, 0.05)
        self.ejecutar_prueba_volumen(40, 0.1)


if __name__ == '__main__':
    unittest.main()