import pulp

# Para: [100, 5, 50, 1, 1, 200]
# Devolver: [0, 2, 5]
def partition(T):
    S1 = []
    S2 = []
    for i in range(len(T)):
        S1.append(pulp.LpVariable('S1_' + str(i), cat='Binary'))
        S2.append(pulp.LpVariable('S2_' + str(i), cat='Binary'))

    problem = pulp.LpProblem('2-partition', pulp.LpMinimize)

    for i in range(len(T)):
        problem += S1[i] + S2[i] == 1

    problem += pulp.LpAffineExpression([(S1[i], T[i]) for i in range(len(T))]) >= pulp.LpAffineExpression([(S2[i], T[i]) for i in range(len(T))])

    problem += pulp.LpAffineExpression([(S1[i], T[i]) for i in range(len(T))])

    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    rs1 = []
    rs2 = []
    for i, T_i in enumerate(T):
        if pulp.value(S1[i]):
            rs1.append(T[i])
        if pulp.value(S2[i]):
            rs2.append(T[i])

    return rs1, rs2

if __name__ == '__main__':
    print(partition([100, 100]))