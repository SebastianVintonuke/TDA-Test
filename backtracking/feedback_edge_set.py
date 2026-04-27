

def feedback_edge_set(grafo):
    componentes = componentes_debilmente_conexas(grafo, grafo.obtener_vertices())
    resultado = []
    for componente in componentes:
        aristas = obtener_aristas(grafo, componente)
        resultado.extend(feedback_edge_set_rec(grafo, componente, aristas, 0, [], aristas[:]))
    return resultado

# Precondición, vertices son una componente conexa
def feedback_edge_set_rec(grafo, componente, aristas, indice, resultado_parcial, mejor_resultado):
    # Poda, ya tengo una solución que funciona borrando menos aristas
    if len(resultado_parcial) >= len(mejor_resultado):
        return mejor_resultado

    # ¡Encontré una mejor solución!
    if not tiene_ciclo(grafo, componente) and len(resultado_parcial) < len(mejor_resultado):
        mejor_resultado = resultado_parcial[:]

    # Por aca ya terminé
    aristas_restantes = len(aristas) - 1 - indice
    if not aristas_restantes:
        return mejor_resultado

    # Pruebo sin sacar la arista, primero esto, ya que si el grafo es acíclico con todas las aristas lo encuentro rapido
    resultado_con = feedback_edge_set_rec(grafo, componente, aristas, indice+1, resultado_parcial, mejor_resultado)
    if len(resultado_con) <= len(mejor_resultado):
        mejor_resultado = resultado_con

    # Pruebo sacando la arista
    candidato = aristas[indice]
    grafo.borrar_arista(candidato[0], candidato[1])
    resultado_parcial.append(candidato)

    resultado_sin = feedback_edge_set_rec(grafo, componente, aristas, indice + 1, resultado_parcial, mejor_resultado)
    if len(resultado_sin) <= len(mejor_resultado):
        mejor_resultado = resultado_sin

    # Restauro el estado
    grafo.agregar_arista(candidato[0], candidato[1])
    resultado_parcial.remove(candidato)

    return mejor_resultado

def obtener_aristas(grafo, componente):
    aristas_componente = set()
    for vertice in componente:
        for adyacente in grafo.adyacentes(vertice):
            aristas_componente.add((vertice, adyacente))
    return list(aristas_componente)





# O(v+e)
def tiene_ciclo(grafo, vertices):
    visitados = set()
    en_pila = set()

    def dfs_hay_ciclo(v):
        visitados.add(v)
        en_pila.add(v)

        for adyacente in grafo.adyacentes(v):
            # Solo consideramos adyacentes que estén dentro del subconjunto de vértices
            if adyacente in vertices:
                if adyacente not in visitados:
                    if dfs_hay_ciclo(adyacente):
                        return True
                elif adyacente in en_pila:
                    return True

        en_pila.remove(v)
        return False

    for v in vertices:
        if v not in visitados:
            if dfs_hay_ciclo(v):
                return True
    return False

# O(v+e)
def componentes_debilmente_conexas(grafo, vertices):
    # Primero construimos un mapa de "predecesores" para poder recorrer el grafo
    # en sentido inverso y tratarlo como no dirigido.
    predecesores = {v: [] for v in vertices}
    for v in vertices:
        for ady in grafo.adyacentes(v):
            if ady in predecesores:
                predecesores[ady].append(v)

    resultado = []
    visitados = set()

    for v in vertices:
        if v not in visitados:
            nueva_componente = []
            # Usamos un BFS para encontrar todos los alcanzables ignorando dirección
            cola = [v]
            visitados.add(v)

            while cola:
                actual = cola.pop(0)
                nueva_componente.append(actual)

                # Sucesores (dirección original)
                for vecino in grafo.adyacentes(actual):
                    if vecino in vertices and vecino not in visitados:
                        visitados.add(vecino)
                        cola.append(vecino)

                # Predecesores (dirección inversa)
                for vecino in predecesores[actual]:
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.append(vecino)

            resultado.append(nueva_componente)

    return resultado


import unittest
from backtracking.grafo import Grafo


class TestFeedbackEdgeSet(unittest.TestCase):

    def setUp(self):
        # Se asume que la clase Grafo está disponible en el scope
        pass

    def test_grafo_vacio(self):
        g = Grafo(dirigido=True)
        res = feedback_edge_set(g)
        self.assertEqual(res, [])

    def test_sin_ciclos(self):
        g = Grafo(dirigido=True)
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "C")
        res = feedback_edge_set(g)
        self.assertEqual(len(res), 0, "No debería eliminar aristas en un DAG")

    def test_ciclo_simple(self):
        # A -> B -> A
        g = Grafo(dirigido=True)
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "A")
        res = feedback_edge_set(g)
        self.assertEqual(len(res), 1, "Debe eliminar 1 arista para romper el ciclo")

        # Verificar que el grafo resultante es acíclico
        for u, v in res:
            g.borrar_arista(u, v)
        self.assertFalse(tiene_ciclo(g, g.obtener_vertices()))

    def test_dos_componentes_separadas(self):
        g = Grafo(dirigido=True)
        # Componente 1: Ciclo A-B-A
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "A")
        # Componente 2: Ciclo C-D-E-C
        g.agregar_arista("C", "D")
        g.agregar_arista("D", "E")
        g.agregar_arista("E", "C")

        res = feedback_edge_set(g)
        self.assertEqual(len(res), 2, "Debe eliminar una arista de cada componente")

    def test_ciclos_entrelazados(self):
        # Grafo donde una sola arista puede romper dos ciclos
        # A -> B, B -> C, C -> A (Ciclo 1)
        # B -> D, D -> B (Ciclo 2)
        # Eliminar (B, A) y (B, D) es una opción, pero (B, C) y (B, D) también.
        # El objetivo es el mínimo.
        g = Grafo(dirigido=True)
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "C")
        g.agregar_arista("C", "A")
        g.agregar_arista("B", "D")
        g.agregar_arista("D", "B")

        res = feedback_edge_set(g)
        # Para este caso, se necesitan 2 aristas (ej: B->C y B->D)
        self.assertEqual(len(res), 2)

        for u, v in res:
            g.borrar_arista(u, v)
        self.assertFalse(tiene_ciclo(g, g.obtener_vertices()))

    def test_componentes_debilmente_conexas(self):
        g = Grafo(dirigido=True)
        # A -> B y C -> B.
        # No hay camino de A a C, pero están débilmente conectados por B.
        g.agregar_arista("A", "B")
        g.agregar_arista("C", "B")
        g.agregar_arista("D", "E")  # Componente separada

        comp = componentes_debilmente_conexas(g, g.obtener_vertices())
        self.assertEqual(len(comp), 2)

        # Verificar que A, B y C están en la misma lista
        comp_abc = next(c for c in comp if "A" in c)
        self.assertTrue(set(["A", "B", "C"]).issubset(set(comp_abc)))

    def test_tiene_ciclo_falso_positivo(self):
        # Caso de "diamante": A -> B, A -> C, B -> D, C -> D
        # No tiene ciclos, pero los nodos se visitan varias veces.
        g = Grafo(dirigido=True)
        g.agregar_arista("A", "B")
        g.agregar_arista("A", "C")
        g.agregar_arista("B", "D")
        g.agregar_arista("C", "D")

        self.assertFalse(tiene_ciclo(g, g.obtener_vertices()))

    def test_grafo_completo_pequeno(self):
        # K3 dirigido (todos con todos)
        g = Grafo(dirigido=True)
        nodes = ["A", "B", "C"]
        for u in nodes:
            for v in nodes:
                if u != v:
                    g.agregar_arista(u, v)

        res = feedback_edge_set(g)
        # Se necesitan eliminar 3 aristas para que sea un DAG (quedaría un orden topológico)
        self.assertEqual(len(res), 3)

        for u, v in res:
            g.borrar_arista(u, v)
        self.assertFalse(tiene_ciclo(g, g.obtener_vertices()))


if __name__ == '__main__':
    unittest.main()