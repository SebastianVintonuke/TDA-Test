import pulp

def inmobiliaria(V):
    J = []
    K = []
    for i, V_i in enumerate(V):
        J.append(pulp.LpVariable('J_' + str(i), cat='Binary'))
        K.append(pulp.LpVariable('K_' + str(i), cat='Binary'))

    problem = pulp.LpProblem('inmobiliaria', pulp.LpMaximize)

    # Busco que solo se pueda comprar un día
    # $\sum_{i} J_i = 1$
    problem += pulp.lpSum(J) == 1

    # Busco que solo se pueda vender un día
    # $\sum_{i} K_i = 1$
    problem += pulp.lpSum(K) == 1

    # Busco maximizar la ganancia, es decir la diferencia entre el dia que se compra y el dia que se vende
    # $max(sum_{i} K_i * V_i - sum_{i} J_i * V_i)$
    problem += pulp.LpAffineExpression([(K[i], V_i) for i, V_i in enumerate(V)]) - pulp.LpAffineExpression([(J[i], V_i) for i, V_i in enumerate(V)])

    # Busco que el número de secuencia del día que se compra sea anterior al del dia que se vende
    # $\sum_{i} J_i * P_i <= \sum_{i} K_i * P_i$
    problem += pulp.LpAffineExpression([(J[P_i], P_i) for P_i, _ in enumerate(V)]) <= pulp.LpAffineExpression([(K[P_i], P_i) for P_i, _ in enumerate(V)])

    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    compro = 0
    vendo = 0
    for i, V_i in enumerate(V):
        if pulp.value(J[i]):
            compro = i
        if pulp.value(K[i]):
            vendo = i

    return compro, vendo












import unittest


class TestInmobiliaria(unittest.TestCase):
    def test_1(self):
        print(inmobiliaria([1,2,3,4,5,6]))

    def test_2(self):
        print(inmobiliaria([6,5,4,3,2,1]))

    def test_3(self):
        print(inmobiliaria([5,1,5,10,5]))