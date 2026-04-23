# Complejidad: O(n log n), el ordenamiento es el término dominante

# ¿El algoritmo implementado encuentra siempre la solución óptima?
# Si, supongamos que tenemos un scheduling A óptimo y un scheduling B no óptimo con dos elementos
# k, j de tal forma que k va antes que j, pero D_k > D_j, entonces:

# F_k = S_i + T_k                 ===>             L_k = S_i + T_k - D_k
# F_j = S_i + T_k + T_j           ===>             L_j = S_i + T_k + T_j - D_j

# Si intercambiamos estas tareas

# F_j = S_i + T_j                 ===>             L_j = S_i + T_j - D_j
# F_k = S_i + T_j + T_k           ===>             L_k = S_i + T_j + T_k - D_k

# L_j es mejor, que antes, ya que: (S_i + T_j - D_j) < (S_i + T_k + T_j - D_j)
# y L_k después del intercambio es mejor que L_j antes de este, ya que D_k > D_j
# (S_i + T_j + T_k - D_k) < (S_i + T_k + T_j - D_j)

# La latencia del recto de elementos no se ve modificada,
# ya que para los anteriores T_k y T_j no intervienen y para los posteriores,
# T_k + T_j = T_j + T_k, es decir el orden no importa

# ¿Por qué se trata de un algoritmo Greedy?
# Porque toma una decision en base a un maximo local con el objetivo de llegar a un maximo global
# En este caso, tomar la tarea con el deadline más proximo, con el objetivo de minimizar todos los deadlines

def minimizar_latencia(L_deadline, T_tareas):

    tarea_deadline = []
    for i in range(len(T_tareas)):
        tarea_deadline.append((T_tareas[i], L_deadline[i]))
    tarea_deadline.sort(key=lambda t: t[1]) # O(n log n)

    resultado = []
    S_i = 0
    for i in tarea_deadline: # O(n)
        T_i = i[0]
        D_i = i[1]
        F_i = S_i + T_i
        if F_i > D_i:
            L_i = F_i - D_i
        else:
            L_i = 0
        resultado.append((T_i, L_i))
        S_i = F_i

    return resultado


def test_minimizar_latencia():
    casos = [
        {
            "T": [3, 2, 1], "D": [6, 8, 9],
            "max_lat_esperada": 0,
            "desc": "Todo a tiempo"
        },
        {
            "T": [5, 10], "D": [8, 10],
            "max_lat_esperada": 5,
            "desc": "Minimizar el gran retraso"
        },
        {
            "T": [2, 10], "D": [100, 10],
            "max_lat_esperada": 0,
            "desc": "Priorizar deadline corto"
        },
        {
            "T": [5, 5], "D": [2, 3],
            "max_lat_esperada": 7,
            "desc": "Ambas con retraso"
        }
    ]

    for i, caso in enumerate(casos):
        # La función debe devolver [(duracion, latencia), ...]
        resultado = minimizar_latencia(caso["D"], caso["T"])

        tiempo_actual = 0
        max_lat_obtenida = 0
        error_calculo = False

        for duracion, latencia in resultado:
            tiempo_actual += duracion
            # Verificamos si la latencia reportada por el alumno es correcta
            # Buscamos el deadline original basado en la duración (simplificado para el test)
            # Nota: Este test asume que no hay duraciones duplicadas con distintos deadlines
            # para validar la cuenta interna.
            idx = -1
            for j in range(len(caso["T"])):
                if caso["T"][j] == duracion and caso["D"][j] not in [x for x in []]:  # Simplificación
                    idx = j

            latencia_real = max(0, tiempo_actual - caso["D"][idx])
            if latencia != latencia_real:
                error_calculo = True

            max_lat_obtenida = max(max_lat_obtenida, latencia)

        if not error_calculo and max_lat_obtenida == caso["max_lat_esperada"]:
            print(f"Test {i + 1} ({caso['desc']}): PASSED ✅")
        else:
            print(f"Test {i + 1} ({caso['desc']}): FAILED ❌")
            print(f"   Max Latencia obtenida: {max_lat_obtenida} | Esperada: {caso['max_lat_esperada']}")
            if error_calculo: print("   ⚠️ Error: La latencia devuelta en la tupla no coincide con el cálculo real.")

if __name__ == '__main__':
    test_minimizar_latencia()