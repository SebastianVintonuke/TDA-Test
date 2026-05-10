import pulp

# Para: [100, 5, 50, 1, 1, 200]
# Devolver: [0, 2, 5]
def juan_el_vago(trabajos):
    y = []
    for i in range(len(trabajos)):
        y.append(pulp.LpVariable('Y_' + str(i), cat='Binary'))

    problem = pulp.LpProblem('juan_el_vago', pulp.LpMaximize)
    for i in range(len(trabajos)):
        for ady in adyacentes(i, trabajos):
            problem += y[i] + y[ady] <= 1

    problem += pulp.LpAffineExpression([(y[i], trabajos[i]) for i in range(len(trabajos))])
    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    res = []
    for i, yi in enumerate(y):
        if pulp.value(yi):
            res.append(i)

    return res


def adyacentes(i, trabajos):
    if i == 0 and len(trabajos) == 1:
        return []
    elif i == 0 and len(trabajos) > 1:
        return [1]
    elif i == len(trabajos)-1:
        return [len(trabajos) - 2]
    elif i >= len(trabajos):
        raise Exception('Unreachable')
    else:
        return [i-1, i+1]


if __name__ == '__main__':
    print(juan_el_vago([100, 5, 50, 1, 1, 200]))