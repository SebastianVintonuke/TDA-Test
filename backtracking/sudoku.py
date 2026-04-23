POSIBILIDADES = [1,2,3,4,5,6,7,8,9]


def resolver_sudoku(matriz):
    casillas = []
    for i_fila, fila in enumerate(matriz):
        for i_columna, celda in enumerate(matriz[i_fila]):
            if matriz[i_fila][i_columna] == 0:
                casillas.append((i_fila, i_columna))
    return resolver_sudoku_rec(matriz, casillas)


def resolver_sudoku_rec(matriz, casillas):
    if not casillas:
        return matriz
    casillas.sort(key=lambda casilla: len(posibilidades_de_en(casilla, matriz)), reverse=True)
    posicion = casillas.pop()
    for candidato in POSIBILIDADES:
        if es_compatible(matriz, candidato, posicion):
            fila, columna = posicion
            matriz[fila][columna] = candidato
            resultado = resolver_sudoku_rec(matriz, casillas)
            if resultado:
                return resultado
            matriz[fila][columna] = 0
    casillas.append(posicion)
    return None


def es_compatible(matriz, numero, posicion):
    return numero in posibilidades_de_en(posicion, matriz)


def posibilidades_de_en(casilla, matriz):
    fila, columna = casilla
    posibilidades = set(POSIBILIDADES)
    # Verificar por fila y columna
    for i in range(len(matriz)):
        posibilidades.discard(matriz[i][columna])
        posibilidades.discard(matriz[fila][i])
    # Verificar por esquinas de cuadrante
    centro_fila = ((fila // 3) * 3) + 1
    centro_columna = ((columna // 3) * 3) + 1
    posibilidades.discard(matriz[centro_fila - 1][centro_columna - 1])
    posibilidades.discard(matriz[centro_fila - 1][centro_columna])
    posibilidades.discard(matriz[centro_fila - 1][centro_columna + 1])
    posibilidades.discard(matriz[centro_fila][centro_columna - 1])
    posibilidades.discard(matriz[centro_fila][centro_columna])
    posibilidades.discard(matriz[centro_fila][centro_columna + 1])
    posibilidades.discard(matriz[centro_fila + 1][centro_columna - 1])
    posibilidades.discard(matriz[centro_fila + 1][centro_columna])
    posibilidades.discard(matriz[centro_fila + 1][centro_columna + 1])
    return posibilidades














import unittest

class TestSudoku(unittest.TestCase):

    def es_valido(self, matriz):
        """Verifica si la matriz de 9x9 es una solución de Sudoku válida."""
        # 1. Verificar filas
        for fila in matriz:
            if not self._bloque_valido(fila): return False

        # 2. Verificar columnas
        for col in range(9):
            columna = [matriz[fila][col] for fila in range(9)]
            if not self._bloque_valido(columna): return False

        # 3. Verificar subgrupos 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrupo = []
                for x in range(3):
                    for y in range(3):
                        subgrupo.append(matriz[i + x][j + y])
                if not self._bloque_valido(subgrupo): return False
        return True

    def _bloque_valido(self, bloque):
        """Verifica que el bloque contenga exactamente los números del 1 al 9."""
        return sorted(bloque) == list(range(1, 10))

    def test_sudoku_facil(self):
        matriz = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 1, 7, 9]
        ]
        resolver_sudoku(matriz)
        self.assertTrue(self.es_valido(matriz), "El Sudoku fácil no se resolvió correctamente")

    def test_sudoku_vacio(self):
        """Un tablero vacío es válido y el backtracking debe llenarlo."""
        matriz = [[0 for _ in range(9)] for _ in range(9)]
        resolver_sudoku(matriz)
        self.assertTrue(self.es_valido(matriz), "No se pudo resolver un tablero vacío")

    def test_sudoku_dificil(self):
        matriz = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 8, 5],
            [0, 0, 1, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 7, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 1, 0, 0],
            [0, 9, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 7, 3],
            [0, 0, 2, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 9]
        ]
        resolver_sudoku(matriz)
        self.assertTrue(self.es_valido(matriz), "El Sudoku difícil no se resolvió correctamente")

    def test_preservacion_de_valores(self):
        """Verifica que los valores originales (distintos de 0) no se modifiquen."""
        original = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        # Copia profunda manual para comparar
        copia_original = [fila[:] for fila in original]

        resolver_sudoku(original)

        for i in range(9):
            for j in range(9):
                if copia_original[i][j] != 0:
                    self.assertEqual(original[i][j], copia_original[i][j],
                                     f"El valor original en ({i},{j}) fue modificado")


if __name__ == '__main__':
    unittest.main()