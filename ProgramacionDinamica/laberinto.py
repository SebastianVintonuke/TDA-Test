
# Ecuación de recurrencia:
#
#         OPT(0,0) = V_0,0
#         OPT(i,0) = OPT(i-1,0) + V_i0
#         OPT(0,j) = OPT(0,j-1) + V_0j
#
#         OPT(i, j) = max( OPT(i-1, j), OPT(i, j-1) ) + V_ij
#
# Complejidad = O(n*m) siendo n el numero de filas de la matriz y m el número de columnas
#
# Si hay "obstáculos", podemos poner un número negativo muy grande, independientemente de como se llega
# de forma que el algoritmo al mirar desde otras casillas si "llego pasando por el obstáculo"
# se vea muy penalizado con respecto a no pasar por ahi
# Notar que utilizar 0 en lugar de un número negativo puede confundirse
# con venir de una casilla que no es un obstáculo,
# pero que aún no ha acumulado, ni tiene por sí misma, valor.
def laberinto(matriz):
    if not matriz:
        return 0
    optimos = c_optimos(matriz)
    return optimos[len(matriz)-1][len(matriz[0])-1]


def c_optimos(matriz):
    n_cantidad_de_filas = len(matriz)
    m_cantidad_de_columnas = len(matriz[0])
    optimos = [ [ 0 for _ in range(m_cantidad_de_columnas) ] for _ in range(n_cantidad_de_filas) ]
    optimos[0][0] = matriz[0][0]

    # Lleno la primera columna, solo se puede llegar por arriba
    for fila in range(1, n_cantidad_de_filas): # O(n-1) = O(n)
        optimos[fila][0] = optimos[fila - 1][0] + matriz[fila][0]

    # Lleno la primera fila, solo se puede llegar por la izquierda
    for columna in range(1, m_cantidad_de_columnas): # O(m-1) = O(m)
        optimos[0][columna] = optimos[0][columna - 1] + matriz[0][columna]

    for fila in range(1, n_cantidad_de_filas): # O(n-1*m-1) = O(n*m)
        for columna in range(1, m_cantidad_de_columnas):
            si_llego_por_arriba = optimos[fila-1][columna]
            si_llego_por_la_izquierda = optimos[fila][columna-1]
            optimos[fila][columna] = max(si_llego_por_arriba, si_llego_por_la_izquierda) + matriz[fila][columna]

    return optimos

def c_solucion(optimos):
    solucion = []
    fila = len(optimos) - 1
    columna = len(optimos[0]) - 1

    while fila >= 0 and columna >= 0:
        if fila == 0 and columna == 0:
            solucion.append((0,0))
            break
        elif fila == 0:
            solucion.append((0,columna))
            columna -= 1
        elif columna == 0:
            solucion.append((fila,0))
            fila -= 1
        else:
            si_llego_por_arriba = optimos[fila - 1][columna]
            si_llego_por_la_izquierda = optimos[fila][columna - 1]
            solucion.append((fila, columna))
            if si_llego_por_arriba > si_llego_por_la_izquierda:
                fila -= 1
            else:
                columna -= 1
    solucion.reverse()
    return solucion










import unittest

class TestLaberinto(unittest.TestCase):

    def test_matriz_basica(self):
        # Camino: 1 -> 4 -> 8 -> 5 -> 3 = 21
        matriz = [
            [1, 2, 3],
            [4, 8, 2],
            [1, 5, 3]
        ]
        self.assertEqual(laberinto(matriz), 21)

    def test_una_sola_fila(self):
        matriz = [[1, 5, 10, 2]]
        self.assertEqual(laberinto(matriz), 18)

    def test_una_sola_columna(self):
        matriz = [[1], [5], [10], [2]]
        self.assertEqual(laberinto(matriz), 18)

    def test_matriz_2x2(self):
        # 10 + 20 + 30 = 60 (por la derecha y luego abajo)
        matriz = [
            [10, 20],
            [5,  30]
        ]
        self.assertEqual(laberinto(matriz), 60)

    def test_valores_negativos(self):
        # La DP debe elegir el camino "menos malo" o el que sume más
        matriz = [
            [10, -5],
            [ 1, -2]
        ]
        # Caminos: (10-5-2) = 3 o (10+1-2) = 9
        self.assertEqual(laberinto(matriz), 9)

    def test_matriz_un_solo_elemento(self):
        matriz = [[42]]
        self.assertEqual(laberinto(matriz), 42)

    def test_matriz_rectangular(self):
        # 3 filas, 2 columnas
        matriz = [
            [1, 10],
            [1, 1],
            [1, 20]
        ]
        # Camino: 1 -> 10 -> 1 -> 20 = 32
        self.assertEqual(laberinto(matriz), 32)

if __name__ == '__main__':
    unittest.main()