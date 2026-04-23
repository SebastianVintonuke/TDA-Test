def colorear(grafo, n):
    vertices = grafo.obtener_vertices()
    # TODO: ordenar los vertices por el grado, influye en algo?

    if not vertices:
        return True

    colores = dict()
    colores[vertices.pop()] = 0
    colores_usados = set()
    colores_usados.add(0)
    return _colorear_rec(grafo, n, vertices, colores, colores_usados)


def _colorear_rec(grafo, n, vertices, colores, colores_usados):
    # Si no quedan vertices por colorear, termine
    if not vertices:
        return True

    candidato = vertices.pop()
    # Pruebo todos los colores
    for color in range(n):
        if es_compatible(grafo, candidato, colores, color):
            fue_usado = color in colores_usados
            if not fue_usado:
                colores_usados.add(color)

            # Si es compatible, sigo esa rama
            colores[candidato] = color
            if _colorear_rec(grafo, n, vertices, colores, colores_usados):
                return True

            # Limpio el estado y sigo con el siguiente color
            del colores[candidato]

            # Poda, si el color era nuevo y ya no me sirve, otros tampoco van a servir
            if not fue_usado:
                colores_usados.discard(color)
                vertices.append(candidato)
                return False

    # Limpio el estado, este vertice no es compatible con ningún color, algún vertice anterior está mal colocado
    vertices.append(candidato)
    return False


def es_compatible(grafo, vertice, colores, color):
    for adyacente in grafo.adyacentes(vertice):
        if adyacente in colores and colores[adyacente] == color:
            return False
    return True















from grafo import Grafo
import time
import random

def test_solucion():
    # Caso 1: Grafo vacío (Siempre es posible)
    g1 = Grafo()
    assert colorear(g1, 1) == True, "Fallo en grafo vacío"

    # Caso 2: Un solo vértice (Posible con 1 color)
    g2 = Grafo()
    g2.agregar_vertice("A")
    assert colorear(g2, 1) == True, "Fallo con un solo vértice"

    # Caso 3: Dos vértices unidos (Requiere 2 colores)
    g3 = Grafo()
    g3.agregar_vertice("A")
    g3.agregar_vertice("B")
    g3.agregar_arista("A", "B")
    assert colorear(g3, 1) == False, "Fallo: aceptó 1 color para una arista"
    assert colorear(g3, 2) == True, "Fallo: no aceptó 2 colores para una arista"

    # Caso 4: Triángulo (Grafo Completo K3)
    # Requiere exactamente 3 colores
    g4 = Grafo()
    for v in ["A", "B", "C"]: g4.agregar_vertice(v)
    g4.agregar_arista("A", "B")
    g4.agregar_arista("B", "C")
    g4.agregar_arista("C", "A")
    assert colorear(g4, 2) == False, "Fallo: un K3 no se puede pintar con 2 colores"
    assert colorear(g4, 3) == True, "Fallo: un K3 se debe poder pintar con 3 colores"

    # Caso 5: Grafo Estrella (Centro unido a todos)
    # Siempre es posible con 2 colores (Bipartito)
    g5 = Grafo()
    g5.agregar_vertice("Centro")
    for i in range(5):
        v = f"V{i}"
        g5.agregar_vertice(v)
        g5.agregar_arista("Centro", v)
    assert colorear(g5, 2) == True, "Fallo: un grafo estrella es bipartito (2 colores)"

    # Caso 6: Ciclo Impar (Pentágono)
    # Requiere 3 colores
    g6 = Grafo()
    vertices = [1, 2, 3, 4, 5]
    for v in vertices: g6.agregar_vertice(v)
    g6.agregar_arista(1, 2)
    g6.agregar_arista(2, 3)
    g6.agregar_arista(3, 4)
    g6.agregar_arista(4, 5)
    g6.agregar_arista(5, 1)
    assert colorear(g6, 2) == False, "Fallo: ciclo impar requiere 3 colores"
    assert colorear(g6, 3) == True, "Fallo: ciclo impar debe funcionar con 3 colores"

    # Caso 7: Grafo Disconexo
    g7 = Grafo()
    g7.agregar_vertice("A")
    g7.agregar_vertice("B")
    g7.agregar_arista("A", "B")
    g7.agregar_vertice("C") # C está aislado
    assert colorear(g7, 2) == True, "Fallo en grafo disconexo"

    # Caso 8: Tardos
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
    assert colorear(g_tardos, 3)

    print("Todos los tests pasaron exitosamente.")


def test_volumen_coloracion():
    # Parámetros del test
    CANT_VERTICES = 50
    PROBABILIDAD_ARISTA = 0.15  # Grafo moderadamente denso
    N_COLORES = 4

    print(f"Generando grafo aleatorio con {CANT_VERTICES} vértices...")
    grafo = Grafo(dirigido=False)

    # Crear vértices
    vertices = [i for i in range(CANT_VERTICES)]
    for v in vertices:
        grafo.agregar_vertice(v)

    # Crear aristas aleatorias
    for i in range(CANT_VERTICES):
        for j in range(i + 1, CANT_VERTICES):
            if random.random() < PROBABILIDAD_ARISTA:
                grafo.agregar_arista(i, j)

    print(f"Iniciando algoritmo de coloración para {N_COLORES} colores...")

    inicio = time.perf_counter()
    # Aquí asumo que la función 'colorear' ya usa la corrección del índice o copia de vértices
    exito = colorear(grafo, N_COLORES)
    fin = time.perf_counter()

    print("-" * 30)
    print(f"Resultado: {'Éxito' if exito else 'No es coloreable con ' + str(N_COLORES) + ' colores'}")
    print(f"Tiempo transcurrido: {fin - inicio:.4f} segundos")
    print("-" * 30)


def test_grafo_no_coloreable_con_3_colores():
    # Un grafo completo de 4 vértices (K4)
    # Todos están unidos con todos. Necesita 4 colores.
    g = Grafo(dirigido=False)
    vertices = ['A', 'B', 'C', 'D']

    # Crear un K4 (Grafo completo)
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            g.agregar_arista(vertices[i], vertices[j])

    # n = 3 colores
    resultado = colorear(g, 3)

    print(f"Resultado obtenido: {resultado}")
    print(f"Resultado esperado: False")

    if resultado == False:
        print("Test PASADO: El algoritmo identificó correctamente que no es coloreable.")
    else:
        print("Test FALLIDO: El algoritmo dijo que era coloreable (True) pero es imposible.")


if __name__ == "__main__":
    test_volumen_coloracion()
    test_grafo_no_coloreable_con_3_colores()
    test_solucion()

