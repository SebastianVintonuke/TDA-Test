import random
from math import sqrt

# O(n log n)
def puntos_mas_cercanos(puntos):
    p_x = sorted(puntos, key=lambda p: p[0]) # O(n log n)
    p_y = sorted(puntos, key=lambda p: p[1]) # O(n log n)

    ubicaciones = {}
    for i_en_px, p in enumerate(p_x): # O(n)
        ubicaciones[p] = [i_en_px, None]
    for i_en_py, p in enumerate(p_y): # O(n)
        ubicaciones[p][1] = i_en_py

    (p_0, p_1) = puntos_mas_cercanos_rec(p_x, p_y, ubicaciones) # O(n log n)
    return p_0, p_1

# Complejidad: O(n log n)
# Teorema Maestro, A = 2, B = 2, C = 1
# Log2(2) = 1 = C => n ^ 1 * log2(n) = n log n
def puntos_mas_cercanos_rec(px, py, ubicaciones):
    if len(px) <= 3:
        if len(px) == 3:
            return puntos_mas_cercanos_entre_3_puntos(px[0], px[1], px[2])
        else:
            return px[0], px[1]

    centro = len(px) // 2
    q = px[:centro] # O(n)
    r = px[centro:] # O(n)

    q_x = q
    r_x = r
    q_y = list(filter(lambda p: ubicaciones[p][0] < centro, py)) # O(n)
    r_y = list(filter(lambda p: ubicaciones[p][0] >= centro, py)) # O(n)

    (q_0, q_1) = puntos_mas_cercanos_rec(q_x, q_y, ubicaciones)
    (r_0, r_1) = puntos_mas_cercanos_rec(r_x, r_y, ubicaciones)

    delta = min(d(q_0, q_1), d(r_0, r_1))
    x_estrella = q_x[len(q_x) - 1][0]
    L = x_estrella # { (x,y) : x = x_estrella }
    S = set(filter(lambda p_i: abs(p_i[0] - L) < delta, px)) # O(n), points in p within distance delta of L

    S_y = list(filter(lambda p: p in S, py)) # O(n)
    ubicaciones_S_y = {}
    for i_en_S_y, p in enumerate(S_y): # O(n)
        ubicaciones_S_y[p] = i_en_S_y

    if len(S_y) >= 2:
        s, s_prima = S_y[0], S_y[1]
    else:
        s, s_prima = None, None
    for punto in S_y: # O(n)
        ubicacion_punto = ubicaciones_S_y[punto]
        siguientes_15_posiciones = S_y[ubicacion_punto + 1: ubicacion_punto + 16] # O(15) = O(1)
        for posicion in siguientes_15_posiciones: # O(15) = O(1)
            if d(punto, posicion) < d(s, s_prima):
                s = punto
                s_prima = posicion

    if s and s_prima and d(s, s_prima) < delta:
        return s, s_prima
    elif d(q_0, q_1) < d(r_0, r_1):
        return q_0, q_1
    else:
        return r_0, r_1

# O(1)
def d(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# O(1)
def puntos_mas_cercanos_entre_3_puntos(p0, p1, p2):
    d_01 = d(p0, p1)
    d_02 = d(p0, p2)
    d_12 = d(p1, p2)
    if d_01 == min(d_01, d_02, d_12):
        return p0, p1
    if d_02 == min(d_01, d_02, d_12):
        return p0, p2
    else:
        return p1, p2









def generar_puntos_unicos(n):
    rango_x = (0, n*10)
    rango_y = (0, n*10)
    if n > (rango_x[1] - rango_x[0] + 1) or n > (rango_y[1] - rango_y[0] + 1):
        raise ValueError("No hay suficientes valores distintos en el rango para generar n puntos")
    xs = random.sample(range(rango_x[0], rango_x[1] + 1), n)
    ys = random.sample(range(rango_y[0], rango_y[1] + 1), n)
    random.shuffle(ys)
    puntos = list(zip(xs, ys))
    return puntos

def menor_distancia_fuerza_bruta(puntos):
    minima_dist = (puntos[0], puntos[1], d(puntos[0], puntos[1]))
    for punto in puntos:
        for otro_punto in puntos:
            if punto == otro_punto:
                continue
            else:
                dist = d(punto, otro_punto)
                if dist < minima_dist[2]:
                    minima_dist = (punto, otro_punto, dist)
    return minima_dist[0], minima_dist[1]

puntos = generar_puntos_unicos(100)
puntos_objetos = [{"x": x, "y": y} for x, y in puntos]
print(puntos_objetos)

