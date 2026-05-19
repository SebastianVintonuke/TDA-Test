
ORIGEN = 0
DESTINO = 1

def red_residual(grafo, flujos):
    aristas = []
    for v in grafo.obtener_vertices():
        for a in grafo.obtener_adyacentes(v):
            aristas.append((v, a))
    _red_residual = grafo.copy()
    for arista in aristas:
        capacidad = grafo.peso_arista(arista[ORIGEN], arista[DESTINO])
        flujo = flujos[arista]
        capacidad_restante = capacidad - flujo
        if not capacidad_restante:
            _red_residual.borrar_arista(arista[ORIGEN], arista[DESTINO])
        else:
            _red_residual.cambiar_peso(arista[ORIGEN], arista[DESTINO], capacidad_restante)
        if flujo:
            _red_residual.agregar_arista(arista[DESTINO], arista[ORIGEN], flujo)
    return _red_residual


