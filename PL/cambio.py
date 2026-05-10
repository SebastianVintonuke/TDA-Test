import pulp


def cambio(monedas, monto):
    y = []
    for m, v_m in enumerate(monedas):
        y.append(pulp.LpVariable('Y_' + str(m), cat='Integer'))

    problem = pulp.LpProblem('cambio', pulp.LpMinimize)

    for m, v_m in enumerate(monedas):
        problem += y[m] >= 0

    problem += pulp.LpAffineExpression([ (y[m], monedas[m]) for m, v_m in enumerate(monedas) ]) == monto

    problem += pulp.lpSum(y)
    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    res = []
    for m, v_m in enumerate(monedas):
        res.extend([v_m] * int(pulp.value(y[m])))

    return res





















import unittest


class TestCambioGreedy(unittest.TestCase):

    def test_cambio_simple(self):
        # Sistema estándar, monto exacto
        monedas = [1, 5, 10, 25]
        monto = 30
        resultado = cambio(monedas, monto)
        # Greedy debería elegir 25 y luego 5
        self.assertEqual(len(resultado), 2)
        self.assertIn(25, resultado)
        self.assertIn(5, resultado)

    def test_cambio_multiples_monedas(self):
        monedas = [1, 2, 5, 10]
        monto = 28
        resultado = cambio(monedas, monto)
        # Esperado: 10, 10, 5, 2, 1
        self.assertEqual(sum(resultado), 28)
        self.assertEqual(len(resultado), 5)
        self.assertEqual(resultado.count(10), 2)

    def test_monedas_desordenadas(self):
        # El algoritmo debe funcionar aunque el input no esté ordenado
        monedas = [5, 1, 10]
        monto = 16
        resultado = cambio(monedas, monto)
        # Esperado: 10, 5, 1
        self.assertEqual(sum(resultado), 16)
        self.assertEqual(len(resultado), 3)

    def test_monto_cero(self):
        self.assertEqual(cambio([1, 5, 10], 0), [])

if __name__ == '__main__':
    unittest.main()