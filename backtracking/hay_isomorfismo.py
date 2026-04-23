def hay_isomorfismo(g1, g2):
    vertices1 = g1.obtener_vertices()
    vertices2 = g2.obtener_vertices()
    vertices1.sort(key=lambda v: len(g1.adyacentes(v)))
    vertices2.sort(key=lambda v: len(g2.adyacentes(v)))

    # Como minimo tienen que tener la misma cantidad de vertices
    if len(vertices1) != len(vertices2):
        return False

    # Además, para un mismo criterio de orden, aunque no resulte en un mapeo válido,
    # cada vertice debe tener la misma cantidad de aristas que su contraparte
    for i in range(len(vertices1)):
        if len(g1.adyacentes(vertices1[i])) != len(g2.adyacentes(vertices2[i])):
            return False

    return hay_isomorfismo_rec(g1, g2, vertices1, dict(),set())


def hay_isomorfismo_rec(g1, g2, vertices_referencia, mapeo, usados):
    if len(vertices_referencia) == 0:
        return True

    referencia = vertices_referencia.pop()
    # Poda, no probar todos los vertices, solo los que podrían funcionar y no fueron usados
    # si en algún momento no hay candidatos, el mapeo no será válido
    candidatos = [
        v for v in g2.obtener_vertices()
        if len(g1.adyacentes(referencia)) == len(g2.adyacentes(v))
           and v not in usados
    ]

    for candidato in candidatos:
        if es_compatible(g1, g2, referencia, candidato, mapeo):
            mapeo[referencia] = candidato
            usados.add(candidato)
            resultado = hay_isomorfismo_rec(g1, g2, vertices_referencia, mapeo, usados)
            if resultado:
                return resultado
            del mapeo[referencia]
            usados.remove(candidato)

    vertices_referencia.append(referencia)
    return False


def es_compatible(g1, g2, referencia, candidato, mapeo):
    adyacentes_a_la_referencia = g1.adyacentes(referencia)
    adyacentes_al_candidato = g2.adyacentes(candidato)
    # Si el mapeo no es compatible con asignaciones previas, el mapeo no será válido
    for adyacente_a_la_referencia in adyacentes_a_la_referencia:
        if adyacente_a_la_referencia in mapeo:
            if mapeo[adyacente_a_la_referencia] not in adyacentes_al_candidato or g1.peso_arista(referencia, adyacente_a_la_referencia) != g2.peso_arista(candidato, mapeo[adyacente_a_la_referencia]):
                return False
    return True















from backtracking.grafo import Grafo
import unittest
import random



class TestIsomorfismo(unittest.TestCase):

    def test_grafos_vacios(self):
        g1 = Grafo()
        g2 = Grafo()
        self.assertTrue(hay_isomorfismo(g1, g2))

    def test_distinta_cantidad_vertices(self):
        g1 = Grafo(vertices_init=[1, 2])
        g2 = Grafo(vertices_init=[1, 2, 3])
        self.assertFalse(hay_isomorfismo(g1, g2))

    def test_isomorfismo_simple_lineal(self):
        # G1: 1-2-3
        g1 = Grafo(vertices_init=[1, 2, 3])
        g1.agregar_arista(1, 2)
        g1.agregar_arista(2, 3)
        # G2: A-C-B
        g2 = Grafo(vertices_init=['A', 'B', 'C'])
        g2.agregar_arista('A', 'C')
        g2.agregar_arista('C', 'B')
        self.assertTrue(hay_isomorfismo(g1, g2))

    def test_mismos_grados_distinta_conectividad(self):
        """
        Caso clásico: Ambos grafos tienen 6 vértices de grado 2.
        G1 son dos triángulos (ciclos de 3).
        G2 es un hexágono (ciclo de 6).
        """
        g1 = Grafo(vertices_init=[1, 2, 3, 4, 5, 6])
        for u, v in [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)]:
            g1.agregar_arista(u, v)

        g2 = Grafo(vertices_init=['A', 'B', 'C', 'D', 'E', 'F'])
        for u, v in [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('F', 'A')]:
            g2.agregar_arista(u, v)

        self.assertFalse(hay_isomorfismo(g1, g2))

    def test_pesos_distintos(self):
        """Misma estructura pero los pesos de las aristas no coinciden."""
        g1 = Grafo(vertices_init=[1, 2])
        g1.agregar_arista(1, 2, peso=5)

        g2 = Grafo(vertices_init=['A', 'B'])
        g2.agregar_arista('A', 'B', peso=10)

        self.assertFalse(hay_isomorfismo(g1, g2))

    def test_grafo_completo_k4(self):
        vertices = [1, 2, 3, 4]
        g1 = Grafo(vertices_init=vertices)
        g2 = Grafo(vertices_init=['a', 'b', 'c', 'd'])

        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                g1.agregar_arista(vertices[i], vertices[j])
                g2.agregar_arista(chr(97 + i), chr(97 + j))

        self.assertTrue(hay_isomorfismo(g1, g2))

    def test_estrellas_con_centro_distinto(self):
        # G1: Centro en 1
        g1 = Grafo(vertices_init=[1, 2, 3, 4])
        g1.agregar_arista(1, 2);
        g1.agregar_arista(1, 3);
        g1.agregar_arista(1, 4)

        # G2: Centro en 'D'
        g2 = Grafo(vertices_init=['A', 'B', 'C', 'D'])
        g2.agregar_arista('D', 'A');
        g2.agregar_arista('D', 'B');
        g2.agregar_arista('D', 'C')

        self.assertTrue(hay_isomorfismo(g1, g2))

    def test_nodos_aislados(self):
        g1 = Grafo(vertices_init=[1, 2, 3])
        g1.agregar_arista(1, 2)  # 3 queda solo

        g2 = Grafo(vertices_init=['A', 'B', 'C'])
        g2.agregar_arista('B', 'C')  # A queda solo

        self.assertTrue(hay_isomorfismo(g1, g2))

    def test_isomorfismo_gran_volumen_desordenado(self):
        """
        Prueba con 100 vértices donde el segundo grafo se construye
        en un orden de inserción totalmente aleatorio.
        """
        n = 100
        nodos_g1 = list(range(n))
        g1 = Grafo(vertices_init=nodos_g1)

        # 1. Crear estructura compleja en G1 (Anillo + Cuerdas)
        aristas = []
        for i in range(n):
            aristas.append((i, (i + 1) % n, 1))

        random.seed(42)
        for _ in range(n):
            u, v = random.sample(nodos_g1, 2)
            if u != v and (u, v) not in aristas:
                aristas.append((u, v, 1))

        for u, v, p in aristas:
            g1.agregar_arista(u, v, p)

        # 2. Preparar G2 con nodos barajados y nombres distintos
        nodos_g2_nombres = [f"NODE_{i}" for i in range(n)]
        mapping = list(range(n))
        random.shuffle(mapping)  # Permutación de los índices

        # Mapeo real: nodo_g1 -> nombre_nodo_g2
        map_g1_a_g2 = {nodos_g1[i]: nodos_g2_nombres[mapping[i]] for i in range(n)}

        # Desordenar el orden en que se agregan los vértices a G2
        nodos_g2_shuffle = nodos_g2_nombres[:]
        random.shuffle(nodos_g2_shuffle)
        g2 = Grafo(vertices_init=nodos_g2_shuffle)

        # 3. Desordenar el orden en que se agregan las aristas a G2
        aristas_g2 = []
        for u, v, p in aristas:
            aristas_g2.append((map_g1_a_g2[u], map_g1_a_g2[v], p))

        random.shuffle(aristas_g2)
        for u, v, p in aristas_g2:
            g2.agregar_arista(u, v, p)

        # 4. Ejecución del test
        # Esto obliga al backtracking a no encontrar la solución por "orden de llegada"
        self.assertTrue(hay_isomorfismo(g1, g2), "Fallo: No detectó isomorfismo en grafos barajados")

    def test_no_isomorfismo_por_un_grado(self):
        """
        Dos grafos grandes casi idénticos, pero a uno se le quita
        una arista para que falle el isomorfismo.
        """
        n = 300
        g1 = Grafo(vertices_init=list(range(n)))
        g2 = Grafo(vertices_init=list(range(n)))

        # Crear caminos idénticos
        for i in range(n - 1):
            g1.agregar_arista(i, i + 1)
            g2.agregar_arista(i, i + 1)

        # Cerrar ciclo en g1 pero no en g2
        g1.agregar_arista(n - 1, 0)

        self.assertFalse(hay_isomorfismo(g1, g2), "Fallo: G1 es un ciclo y G2 es un camino")


if __name__ == '__main__':
    unittest.main()