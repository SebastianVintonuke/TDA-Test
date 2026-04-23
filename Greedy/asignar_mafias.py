
# Complejidad: O(n log n), el ordenamiento es el término dominante

# ¿El algoritmo da la solución óptima siempre?
# Misma demostración que el algoritmo de charlas

# ¿Por qué se trata de un algoritmo Greedy?
# Porque toma una decision en base a un maximo local con el objetivo de llegar a un maximo global
# en este caso, otorgar el permiso que termina primero con la intención de dejar el
# mayor espacio restante posible en cada paso, con el objetivo de entregar la mayor cantidad de permisos posibles
def asignar_mafias(pedidos):
    candidatos = sorted(pedidos, key=lambda pedido: pedido[1])  # O(n log n)
    pedidos_tomados = []
    ultimo_tomado = None
    for indice, candidato in enumerate(candidatos): # O(n)
        if not ultimo_tomado:
            pedidos_tomados.append(candidato)
            ultimo_tomado = candidato
        elif candidato[0] < ultimo_tomado[1]:
            continue
        else:
            pedidos_tomados.append(candidato)
            ultimo_tomado = candidato
    return pedidos_tomados







def test_asignar_mafias():
    casos = [
        {
            "input": [(1, 3.5), (3.3333, 8), (4, 10)],
            "expected_count": 2,
            "desc": "Dos pedidos compatibles"
        },
        {
            "input": [(1, 10), (2, 3), (4, 5)],
            "expected_count": 2,
            "desc": "Pedidos cortos dentro de uno largo"
        },
        {
            "input": [(1, 2), (2, 3), (3, 4)],
            "expected_count": 3,
            "desc": "Límites exactos"
        },
        {
            "input": [(1, 5), (1, 5), (1, 5)],
            "expected_count": 1,
            "desc": "Mismo rango repetido"
        },
        {
            "input": [(1, 4), (2, 5), (4, 6)],
            "expected_count": 2,
            "desc": "Selección de extremos"
        },
        {
            "input": [(10, 15), (1, 100), (2, 5), (6, 9)],
            "expected_count": 3,
            "desc": "Múltiples intervalos"
        }
    ]

    for i, caso in enumerate(casos):
        resultado = asignar_mafias(caso["input"])

        # 1. Verificar cantidad
        count_ok = len(resultado) == caso["expected_count"]

        # 2. Verificar que no haya solapamientos en el resultado
        resultado_ordenado = sorted(resultado, key=lambda x: x[0])
        solapamiento = False
        for j in range(len(resultado_ordenado) - 1):
            if resultado_ordenado[j][1] > resultado_ordenado[j + 1][0]:
                solapamiento = True
                break

        # 3. Verificar que los pedidos existan en el input original
        existencia_ok = all(p in caso["input"] for p in resultado)

        if count_ok and not solapamiento and existencia_ok:
            print(f"Test {i + 1} ({caso['desc']}): PASSED ✅")
        else:
            print(f"Test {i + 1} ({caso['desc']}): FAILED ❌")
            if not count_ok:
                print(f"   Cantidad incorrecta: {len(resultado)} (esperaba {caso['expected_count']})")
            if solapamiento:
                print(f"   Error: El resultado contiene pedidos que se solapan.")
            if not existencia_ok:
                print(f"   Error: El resultado contiene pedidos que no estaban en la lista original.")

if __name__ == '__main__':
    test_asignar_mafias()