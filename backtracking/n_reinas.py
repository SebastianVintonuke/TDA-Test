def nreinas(n):
    reinas = []
    columnas_usadas = set()
    return nreinas_rec(n, reinas, 0, columnas_usadas)

def nreinas_rec(n, reinas, fila, columnas_usadas):
    if fila == n:
        return reinas # Encontré las n reinas

    for columna in range(n):
        if columna in columnas_usadas:
            continue # Poda por columna

        candidato = (fila, columna)
        # Si es compatible, sigo por esa rama
        if es_compatible_con(reinas, candidato):
            reinas.append(candidato)
            columnas_usadas.add(columna)
            resultado = nreinas_rec(n, reinas, fila + 1, columnas_usadas)

            if resultado:
                return resultado

            # No funciono por aca, limpio el estado
            reinas.pop()
            columnas_usadas.remove(columna)
    return []

def es_compatible_con(reinas_actuales, reina_nueva):
    for reina_actual in reinas_actuales:
        if abs(reina_actual[0] - reina_nueva[0]) == abs(reina_actual[1] - reina_nueva[1]):
            return False # Están en la misma diagonal
    return True







import unittest

class TestNReinas(unittest.TestCase):

    def es_valida(self, solucion, n):
        # 1. Verificar cantidad de reinas
        if len(solucion) != n:
            return False

        for i in range(len(solucion)):
            for j in range(i + 1, len(solucion)):
                r1_fila, r1_col = solucion[i]
                r2_fila, r2_col = solucion[j]

                # 2. Verificar filas y columnas
                if r1_fila == r2_fila or r1_col == r2_col:
                    return False

                # 3. Verificar diagonales
                if abs(r1_fila - r2_fila) == abs(r1_col - r2_col):
                    return False
        return True

    def test_n4(self):
        n = 4
        resultado = nreinas(n)
        self.assertTrue(self.es_valida(resultado, n), f"Solución inválida para N={n}: {resultado}")

    def test_n8(self):
        n = 8
        resultado = nreinas(n)
        self.assertTrue(self.es_valida(resultado, n), f"Solución inválida para N={n}: {resultado}")

    def test_rango_coordenadas(self):
        n = 4
        resultado = nreinas(n)
        for fila, col in resultado:
            self.assertTrue(0 <= fila < n and 0 <= col < n, f"Coordenada ({fila}, {col}) fuera de rango para N={n}")

    def test_x(self):
        print(nreinas(20))

if __name__ == '__main__':
    unittest.main()
