def knight_tour(n):
    casillas_donde_puedo_llegar = dict()
    for casilla in tablero(n):
        casillas_donde_puedo_llegar[casilla] = casillas_donde_puedo_llegar_a_partir_de(n, casilla)

    for casilla in tablero(n):
        resultado = knight_tour_rec(n, casillas_donde_puedo_llegar, [casilla], {casilla})
        if resultado:
            return resultado
    return False


def knight_tour_rec(n, casillas_donde_puedo_llegar, camino, visitados):
    if len(camino) == n*n:
        return camino

    ultimo = camino[-1]
    candidatos = casillas_donde_puedo_llegar[ultimo]
    candidatos.sort(key=lambda casilla: len(casillas_donde_puedo_llegar[casilla]))
    for candidato in candidatos:
        if candidato in visitados:
            continue
        camino.append(candidato)
        visitados.add(candidato)
        resultado = knight_tour_rec(n, casillas_donde_puedo_llegar, camino, visitados)
        if resultado:
            return resultado
        camino.pop()
        visitados.remove(candidato)
    return False


def casillas_donde_puedo_llegar_a_partir_de(n, casilla):
    fila, columna = casilla
    casillas_donde_puedo_llegar = [
        (fila - 1, columna - 2),
        (fila - 1, columna + 2),
        (fila + 1, columna - 2),
        (fila + 1, columna + 2),
        (fila - 2, columna - 1),
        (fila - 2, columna + 1),
        (fila + 2, columna - 1),
        (fila + 2, columna + 1)
    ]
    return [casilla for casilla in casillas_donde_puedo_llegar if 0 <= casilla[0] < n and 0 <= casilla[1] < n]


def tablero(n):
    for fila in range(n):
        for columna in range(n):
            yield fila, columna



import unittest

class TestKnightTour(unittest.TestCase):

    def test_board_size_1(self):
        """Un tablero de 1x1 es trivialmente válido (el caballo ya está en la única casilla)."""
        self.assertTrue(knight_tour(1))

    def test_board_size_2(self):
        """En un tablero de 2x2 el caballo no tiene movimientos posibles."""
        self.assertFalse(knight_tour(2))

    def test_board_size_3(self):
        """En un tablero de 3x3 no existe una solución que recorra todas las casillas."""
        self.assertFalse(knight_tour(3))

    def test_board_size_4(self):
        """En un tablero de 4x4 no existe una solución de recorrido completo."""
        self.assertFalse(knight_tour(4))

    def test_board_size_5(self):
        """5x5 es el tablero más pequeño donde existe una solución de recorrido abierto."""
        self.assertTrue(knight_tour(5))

    def test_board_size_6(self):
        """Un tablero de 6x6 tiene múltiples soluciones de backtracking."""
        self.assertTrue(knight_tour(6))

    def test_board_size_8(self):
        """El tablero estándar de ajedrez tiene solución (Nota: puede ser lento sin optimizaciones)."""
        self.assertTrue(knight_tour(31))

if __name__ == '__main__':
    unittest.main()

