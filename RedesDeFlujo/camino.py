from backtracking.grafo import Grafo
from collections import deque

def camino_de_aumento(red_residual, s, t):
    padres = bfs(red_residual, s)
    if t not in padres:
        return None
    aristas = []
    actual = t
    while actual != s:
        aristas.append((padres[actual], actual))
        actual = padres[actual]
    aristas.reverse()
    return aristas


def bfs(red_residual, s):
    visitados = set()
    padres = {}
    por_visitar = deque([s])
    while por_visitar:
        vertice = por_visitar.popleft()
        for adyacente in red_residual.adyacentes(vertice):
            if adyacente not in visitados:
                padres[adyacente] = vertice
                visitados.add(adyacente)
                por_visitar.append(adyacente)
    return padres