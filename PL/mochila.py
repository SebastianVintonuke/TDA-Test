import pulp

VALOR = 0
PESO = 1

def mochila(elementos, W):
    y = []
    for i, e_i in enumerate(elementos):
        y.append(pulp.LpVariable('Y_' + str(i), cat='Binary'))

    problem = pulp.LpProblem('cambio', pulp.LpMaximize)

    problem += pulp.LpAffineExpression([(y[i], e_i[PESO]) for i, e_i in enumerate(elementos)]) <= W

    problem += pulp.LpAffineExpression([(y[i], e_i[VALOR]) for i, e_i in enumerate(elementos)])

    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    res = []
    for i, e_i in enumerate(elementos):
        if pulp.value(y[i]):
            res.append(e_i)

    return res





def test_mochila_greedy():
    casos = [
        {
            "W": 50,
            "elementos": [(60, 10), (100, 20), (120, 30)],
            "expected_val": 220,  # 100 + 120
            "desc": "Básico (entran los mejores)"
        },
    ]

    for i, caso in enumerate(casos):
        resultado = mochila(caso["elementos"], caso["W"])

        # Validamos que no exceda el peso
        peso_total = sum(e[1] for e in resultado)
        valor_total = sum(e[0] for e in resultado)

        if peso_total <= caso["W"] and valor_total == caso["expected_val"]:
            print(f"Test {i + 1} ({caso['desc']}): PASSED ✅")
        else:
            print(f"Test {i + 1} ({caso['desc']}): FAILED ❌")
            print(f"   Obtenido: {resultado} (Valor: {valor_total}, Peso: {peso_total})")
            print(f"   Esperado Valor: {caso['expected_val']} | Capacidad Máxima: {caso['W']}")

if __name__ == '__main__':
    test_mochila_greedy()