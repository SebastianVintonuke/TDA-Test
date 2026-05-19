from backtracking.grafo import Grafo
from collections import deque

ORIGEN = 0
DESTINO = 1

def ford_fulkerson(grafo, s, t):
    flujos = {}
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            flujos[(v, w)] = 0
    grafo_residual = grafo.copy()
    camino = obtener_camino(grafo_residual, s, t)
    while camino:
        flujo_maximo = min(map(lambda arista: grafo_residual.peso_arista(arista[ORIGEN], arista[DESTINO]), camino))
        for arista in camino:
            if arista in flujos:
                flujos[arista] += flujo_maximo
            else:
                contraria = (arista[DESTINO], arista[ORIGEN])
                flujos[contraria] -= flujo_maximo
            actualizar_grafo_residual(grafo_residual, arista[ORIGEN], arista[DESTINO], flujo_maximo)
        camino = obtener_camino(grafo_residual, s, t)
    return flujos

def obtener_camino(grafo_residual, fuente, sumidero):
    padres = bfs(grafo_residual, fuente, sumidero)
    if sumidero not in padres:
        return None
    camino_aristas = []
    actual = sumidero
    while actual != fuente:
        camino_aristas.append((padres[actual], actual))
        actual = padres[actual]
    camino_aristas.reverse()
    return camino_aristas

def bfs(_grafo, s, t):
    visitados = set()
    padres = {}
    por_visitar = deque()
    por_visitar.append(s)
    while por_visitar:
        vertice = por_visitar.popleft()
        adyacentes = _grafo.adyacentes(vertice)
        for adyacente in adyacentes:
            if not adyacente in visitados:
                padres[adyacente] = vertice
                visitados.add(adyacente)
                por_visitar.append(adyacente)
        if t in visitados:
            break
    return padres

def actualizar_grafo_residual(grafo_residual, u, v, valor):
    peso_anterior = grafo_residual.peso_arista(u, v)
    if peso_anterior == valor:
        grafo_residual.borrar_arista(u, v)
    else:
        grafo_residual.cambiar_peso(u, v, peso_anterior - valor)
    if not grafo_residual.estan_unidos(v, u):
        grafo_residual.agregar_arista(v, u, valor)
    else:
        grafo_residual.cambiar_peso(v, u, peso_anterior + valor)

def main():
    _grafo = Grafo(dirigido=True, vertices_init=["Fu", "J", "K", "A", "F", "C", "E", "Su"])
    _grafo.agregar_arista("Fu", "J", 1)
    _grafo.agregar_arista("Fu", "A", 8)
    _grafo.agregar_arista("J", "K", 1)
    _grafo.agregar_arista("A", "F", 1)
    _grafo.agregar_arista("A", "C", 10)
    _grafo.agregar_arista("K", "F", 1)
    _grafo.agregar_arista("F", "Su", 1)
    _grafo.agregar_arista("C", "E", 9)
    _grafo.agregar_arista("E", "Su", 13)
    resultado = ford_fulkerson(_grafo, "Fu", "Su")
    print(resultado)

if __name__ == '__main__':
    main()



"""
def main():
    _grafo = Grafo(dirigido=True, vertices_init=["super_fuente", "S", "T", "U", "V", "W", "X", "Z", "ZU", "UZ"])
    _grafo.agregar_arista("super_fuente", "S", 9)
    _grafo.agregar_arista("super_fuente", "X", 3)
    _grafo.agregar_arista("S", "V", 6)
    _grafo.agregar_arista("S", "U", 3)
    _grafo.agregar_arista("V", "T", 3)
    _grafo.agregar_arista("V", "W", 1)
    _grafo.agregar_arista("W", "T", 6)
    _grafo.agregar_arista("U", "W", 6)
    _grafo.agregar_arista("X", "Z", 3)
    _grafo.agregar_arista("Z", "W", 1)
    _grafo.agregar_arista("U", "UZ", 2)
    _grafo.agregar_arista("UZ", "Z", 2)
    _grafo.agregar_arista("Z", "ZU", 4)
    _grafo.agregar_arista("ZU", "U", 4)
    resultado = ford_fulkerson(_grafo, "super_fuente", "T")
    print(resultado)
"""