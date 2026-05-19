from backtracking.grafo import Grafo
from collections import deque

ORIGEN = 0
DESTINO = 1

def flujo_lineal_V3(grafo, s, t, flujos, arista):
    grafo_residual = red_residual(grafo, flujos) # O(V+E)

    hay_capacidad_restante = grafo_residual.estan_unidos(arista[ORIGEN], arista[DESTINO]) # O(1)
    if hay_capacidad_restante: # Ya sobra capacidad, aumentarla no cambia nada
        return flujos

    grafo_residual.agregar_arista(arista[ORIGEN], arista[DESTINO], 1) # La arista no tenia que existir porque no había capacidad, la creo para aumentar en 1

    camino = camino_de_aumento(grafo_residual, s, t) # O(V+E)
    if not camino: # Aumente la capacidad aca, pero el cuello de botella está en otro lado
        return flujos

    for arista_camino in camino:
        if arista_camino in flujos:
            flujos[arista_camino] += 1
        else:
            arista_opuesta = (arista_camino[DESTINO], arista_camino[ORIGEN])
            flujos[arista_opuesta] -= 1
    return flujos

# O(V+E)
def flujo_lineal(grafo, s, t, flujos, arista):
    grafo_residual = red_residual(grafo, flujos) # O(V+E)
    camino = camino_de_aumento(grafo_residual, arista[ORIGEN], t) # O(V+E)
    if not camino:
        return flujos
    for arista_camino in camino:
        flujos[arista_camino] += 1
    return flujos

# O(V+E)
def red_residual(grafo, flujos):
    aristas = []
    for v in grafo.obtener_vertices():
        for a in grafo.obtener_adyacentes(v):
            aristas.append((v, a)) # O(V+E)
    grafo_residual = grafo.copy()
    for arista in aristas: # O(E)
        capacidad = grafo.peso_arista(arista[ORIGEN], arista[DESTINO]) # O(1)
        flujo = flujos[arista] # O(1)
        capacidad_restante = capacidad - flujo # O(1)
        if not capacidad_restante:
            grafo_residual.borrar_arista(arista[ORIGEN], arista[DESTINO]) # O(1)
        else:
            grafo_residual.cambiar_peso(arista[ORIGEN], arista[DESTINO], capacidad_restante) # O(1)
        if flujo:
            grafo_residual.agregar_arista(arista[DESTINO], arista[ORIGEN], flujo) # O(1)
    return grafo_residual

# O(V+E)
def camino_de_aumento(grafo_residual, s, t):
    padres = bfs(grafo_residual, s) # O(V+E)
    if t not in padres:
        return None
    aristas = []
    actual = t
    while actual != s: # O(V)
        aristas.append((padres[actual], actual)) # O(1)
        actual = padres[actual] # O(1)
    aristas.reverse() # O(E)
    return aristas

# O(V+E)
def bfs(grafo, s):
    visitados = set()
    padres = {}
    por_visitar = deque([s])
    while por_visitar: # O(V)
        vertice = por_visitar.popleft() # O(1)
        for adyacente in grafo.adyacentes(vertice): # O(V+E)
            if adyacente not in visitados:
                padres[adyacente] = vertice # O(1)
                visitados.add(adyacente) # O(1)
                por_visitar.append(adyacente) # O(1)
    return padres