def camino_hamiltoniano(grafo):
    vertices = grafo.obtener_vertices()
    if not vertices:
        return []
    vertices.sort(key=lambda v: len(grafo.adyacentes(v)))
    for vertice in vertices:
        camino = camino_hamiltoniano_rec(grafo, len(vertices), [vertice], {vertice})
        if camino:
            return camino
    return []


def camino_hamiltoniano_rec(grafo, len_vertices, camino, visitados):
    if len_vertices == len(camino):
        return camino

    ultimo = camino[-1]
    candidatos = [v for v in grafo.adyacentes(ultimo) if v not in visitados]
    for candidato in candidatos:
        camino.append(candidato)
        visitados.add(candidato)
        resultado = camino_hamiltoniano_rec(grafo, len_vertices, camino, visitados)
        if resultado:
            return resultado
        camino.pop()
        visitados.remove(candidato)
    return []















import unittest
import time
import random
from backtracking.grafo import Grafo

def es_camino_hamiltoniano_valido(grafo, camino):
    vertices = grafo.obtener_vertices()
    if len(camino) != len(vertices):
        return False

    # Verificar que todos los vértices del grafo estén en el camino
    if set(camino) != set(vertices):
        return False

    # Verificar que existan aristas entre vértices consecutivos en el camino
    for i in range(len(camino) - 1):
        if not grafo.estan_unidos(camino[i], camino[i + 1]):
            return False

    return True


def generar_grafo_obstaculos(n, densidad_ruido=0.6):
    """
    Crea un grafo con un camino hamiltoniano garantizado (0-1-2-...-n-1)
    pero añade aristas adicionales hacia atrás y hacia nodos aleatorios
    para forzar la exploración de caminos inválidos.
    """
    g = Grafo(dirigido=False)
    for i in range(n):
        g.agregar_vertice(i)

    # Camino hamiltoniano garantizado
    for i in range(n - 1):
        g.agregar_arista(i, i + 1)

    # Añadir aristas de "ruido" para crear opciones inválidas
    # Conectamos nodos con sus predecesores lejanos para crear ciclos
    for i in range(n):
        for j in range(i - 2):  # Aristas hacia atrás que no ayudan al camino
            if random.random() < densidad_ruido:
                if not g.estan_unidos(i, j):
                    g.agregar_arista(i, j)

    return g

class TestCaminoHamiltoniano(unittest.TestCase):

    def test_grafo_vacio(self):
        g = Grafo(dirigido=False)
        resultado = camino_hamiltoniano(g)
        self.assertEqual(resultado, [])

    def test_un_solo_vertice(self):
        g = Grafo(dirigido=False)
        g.agregar_vertice("A")
        resultado = camino_hamiltoniano(g)
        self.assertEqual(resultado, ["A"])

    def test_dos_vertices_unidos(self):
        g = Grafo(dirigido=False)
        g.agregar_vertice("A")
        g.agregar_vertice("B")
        g.agregar_arista("A", "B")
        resultado = camino_hamiltoniano(g)
        self.assertTrue(es_camino_hamiltoniano_valido(g, resultado))

    def test_grafo_lineal(self):
        g = Grafo(dirigido=False)
        vertices = ["A", "B", "C", "D"]
        for v in vertices:
            g.agregar_vertice(v)
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "C")
        g.agregar_arista("C", "D")

        resultado = camino_hamiltoniano(g)
        self.assertTrue(es_camino_hamiltoniano_valido(g, resultado))

    def test_grafo_completo_K4(self):
        g = Grafo(dirigido=False)
        vertices = ["A", "B", "C", "D"]
        for v in vertices:
            g.agregar_vertice(v)
        # Conectar todos con todos
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                g.agregar_arista(vertices[i], vertices[j])

        resultado = camino_hamiltoniano(g)
        self.assertTrue(es_camino_hamiltoniano_valido(g, resultado))

    def test_no_existe_camino_desconectado(self):
        g = Grafo(dirigido=False)
        g.agregar_vertice("A")
        g.agregar_vertice("B")
        g.agregar_vertice("C")
        g.agregar_arista("A", "B")
        # C está aislado
        resultado = camino_hamiltoniano(g)
        self.assertEqual(resultado, [])

    def test_no_existe_camino_en_estrella(self):
        # Un centro conectado a 3 hojas. No se puede recorrer sin repetir el centro.
        g = Grafo(dirigido=False)
        g.agregar_vertice("Centro")
        for v in ["H1", "H2", "H3"]:
            g.agregar_vertice(v)
            g.agregar_arista("Centro", v)

        resultado = camino_hamiltoniano(g)
        self.assertEqual(resultado, [])

    def test_volumen_con_ruido(self):
        # El rango 10-25 suele ser el punto de quiebre para algoritmos no optimizados
        tamanos = [900]

        print(f"{'Vértices':<10} | {'Aristas':<10} | {'Tiempo (s)':<12} | {'Estado'}")
        print("-" * 50)

        for n in tamanos:
            g = generar_grafo_obstaculos(n)

            # Contar aristas totales para referencia
            cant_aristas = 0
            v_lista = g.obtener_vertices()
            for i in range(len(v_lista)):
                cant_aristas += len(g.adyacentes(v_lista[i]))
            cant_aristas //= 2  # Grafo no dirigido

            inicio = time.time()
            resultado = camino_hamiltoniano(g)
            fin = time.time()

            tiempo_total = fin - inicio

            # Validación del resultado
            if len(resultado) == n:
                estado = "OK"
            else:
                estado = "No encontrado"

            print(f"{n:<10} | {cant_aristas:<10} | {tiempo_total:<12.5f} | {estado}")


if __name__ == '__main__':
    unittest.main()




