
def max_sumatoria_n(lista, n):
    return max_sumatoria_n_rec(lista, n, 0, [], 0, [], 0)[0]

def max_sumatoria_n_rec(lista, n, indice, sumandos, sumatoria, max_sumandos, max_sumatoria):
    # Poda ya me pase
    if sumatoria > n:
        return max_sumandos, max_sumatoria

    # Resultado optimo
    if sumatoria == n:
        return sumandos, sumatoria

    # Nuevo maximo
    if max_sumatoria < sumatoria < n:
        max_sumandos = sumandos[:]
        max_sumatoria = sumatoria

    # LLegue al final
    if len(lista) == indice:
        return max_sumandos, max_sumatoria

    candidato = lista[indice]

    # Pruebo poner
    sumandos.append(candidato)
    sumatoria += candidato

    res_sumandos_con, res_sumatoria_con = max_sumatoria_n_rec(lista, n, indice + 1, sumandos, sumatoria, max_sumandos, max_sumatoria)
    if res_sumatoria_con == n:
        return res_sumandos_con, res_sumatoria_con
    elif res_sumatoria_con > max_sumatoria:
        max_sumandos = res_sumandos_con
        max_sumatoria = res_sumatoria_con

    # Restauro el estado
    sumandos.pop()
    sumatoria -= candidato

    # Pruebo no poner
    res_sumandos_sin, res_sumatoria_sin = max_sumatoria_n_rec(lista, n, indice + 1, sumandos, sumatoria, max_sumandos, max_sumatoria)
    if res_sumatoria_sin == n:
        return res_sumandos_sin, res_sumatoria_sin
    elif res_sumatoria_sin > max_sumatoria:
        max_sumandos = res_sumandos_sin
        max_sumatoria = res_sumatoria_sin

    return max_sumandos, max_sumatoria






import unittest

class TestMaxSumatoriasN(unittest.TestCase):

    def test_suma_exacta_existe(self):
        """Si existe una suma exacta, debe devolverla."""
        lista = [1, 5, 10, 20]
        n = 15
        resultado = max_sumatoria_n(lista, n)
        # 10 + 5 = 15
        self.assertEqual(sum(resultado), 15)
        self.assertTrue(set(resultado).issubset(set(lista)))

    def test_suma_maxima_sin_pasarse(self):
        """Si no hay suma exacta, debe devolver la mayor posible menor a n."""
        lista = [10, 20, 30]
        n = 25
        resultado = max_sumatoria_n(lista, n)
        # La mejor suma es 20 (30 se pasa, 10 es menor)
        self.assertEqual(sum(resultado), 20)
        self.assertEqual(resultado, [20])

    def test_aproximacion_con_multiples_elementos(self):
        """Debe elegir la combinación que más se acerque a n."""
        lista = [8, 15, 3]
        n = 12
        resultado = max_sumatoria_n(lista, n)
        # 8 + 3 = 11 (es mejor que 8 solo o que 15 que se pasa)
        self.assertEqual(sum(resultado), 11)
        self.assertCountEqual(resultado, [8, 3])

    def test_n_muy_pequeno(self):
        """Si todos los elementos son mayores a n, debería devolver conjunto vacío (suma 0)."""
        lista = [10, 20, 30]
        n = 5
        resultado = max_sumatoria_n(lista, n)
        self.assertEqual(resultado, [])

    def test_lista_vacia(self):
        """Con lista vacía, la mejor suma es 0."""
        self.assertEqual(max_sumatoria_n([], 10), [])

    def test_n_exacto_con_toda_la_lista(self):
        """Debe devolver todos los elementos si la suma total es exactamente n."""
        lista = [1, 2, 3]
        n = 6
        resultado = max_sumatoria_n(lista, n)
        self.assertCountEqual(resultado, [1, 2, 3])

if __name__ == '__main__':
    unittest.main()