import pulp


def k_cercanos(arreglo, elemento, k):
    y = []
    d = distancias(arreglo, elemento)
    for i, _ in enumerate(arreglo):
        y.append(pulp.LpVariable('Y_' + str(i), cat='Integer'))

    problem = pulp.LpProblem('k_cercanos', pulp.LpMinimize)

    problem += pulp.lpSum(y) <= k

    M = max(d)
    problem += pulp.LpAffineExpression([ (y[i], d[i]) for i, _ in enumerate(arreglo) ]) - pulp.LpAffineExpression([ (y[i], M) for i, _ in enumerate(arreglo) ])

    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    res = []
    for i, _ in enumerate(arreglo):
        if pulp.value(y[i]):
            res.append(i)
    return res

def distancias(arreglo, elemento):
    return []