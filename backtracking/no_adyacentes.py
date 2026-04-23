from backtracking.grafo import Grafo


def no_adyacentes(grafo, n):
    'Devolver una lista con los n vértices, o None de no ser posible'
    if n == 0:
        return []

    vertices = grafo.obtener_vertices()
    return _no_adyacentes_rec(grafo, n, vertices, [])


def _no_adyacentes_rec(grafo, n, restantes, subconjunto):
    # Encontré uno
    if len(subconjunto) == n:
        return subconjunto

    # No llego
    if not restantes or len(subconjunto) + len(restantes) < n:
        return None

    candidato = restantes.pop()
    if es_compatible(grafo, subconjunto, candidato):
        # Pruebo poner
        subconjunto.append(candidato)
        resultado = _no_adyacentes_rec(grafo, n, restantes, subconjunto)
        if resultado:
            return resultado
        # Puse, no anda, lo saco
        subconjunto.pop()

    # Pruebo no poner
    resultado = _no_adyacentes_rec(grafo, n, restantes, subconjunto)
    if resultado:
        return resultado
    else:
        restantes.append(candidato)
        return None


def es_compatible(grafo, subconjunto, candidato):
    for v in grafo.adyacentes(candidato):
        if v in subconjunto:
            return False
    return True











































def test_no_adyacentes():
    # --- Test 1: Grafo Completo K3 ---
    g_completo = Grafo(vertices_init=[1, 2, 3])
    g_completo.agregar_arista(1, 2)
    g_completo.agregar_arista(2, 3)
    g_completo.agregar_arista(3, 1)

    assert no_adyacentes(g_completo, 1) is not None
    assert no_adyacentes(g_completo, 2) is None, "En K3 no hay 2 vértices independientes"

    # --- Test 2: Grafo Camino P4 (1-2-3-4) ---
    g_camino = Grafo(vertices_init=[1, 2, 3, 4])
    g_camino.agregar_arista(1, 2)
    g_camino.agregar_arista(2, 3)
    g_camino.agregar_arista(3, 4)

    res_p4 = no_adyacentes(g_camino, 2)
    assert res_p4 is not None
    assert len(res_p4) == 2
    assert not g_camino.estan_unidos(res_p4[0], res_p4[1])

    # --- Test 3: Grafo Estrella (0 es el centro) ---
    g_estrella = Grafo(vertices_init=[0, 1, 2, 3, 4])
    for i in range(1, 5):
        g_estrella.agregar_arista(0, i)

    res_estrella = no_adyacentes(g_estrella, 4)
    assert res_estrella is not None
    assert set(res_estrella) == {1, 2, 3, 4}

    # --- Test 4: Grafo Desconectado ---
    g_desc = Grafo(vertices_init=[1, 2, 3])
    # Sin aristas
    res_desc = no_adyacentes(g_desc, 3)
    assert res_desc is not None
    assert len(res_desc) == 3

    # --- Test 5: n = 0 ---
    assert no_adyacentes(g_camino, 0) == []

    # --- Test 6: n = 4 ---
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
    res_p6 = no_adyacentes(g_tardos, 3)
    assert res_p6 is not None
    assert len(res_p6) == 3


    print("Todos los tests pasaron exitosamente.")


if __name__ == "__main__":
    test_no_adyacentes()