

# Complejidad: O(n log n), el ordenamiento es el término dominante

# ¿El algoritmo implementado encuentra siempre la solución óptima?
# No, contraejemplo: elementos [(95,9),(50,5),(50,5)] W 10
# 50 / 5 = 10
# 95 / 9 = 10.5
# El algoritmo elige (95,9), maximo valor 95, si elegía [(50,5), (50,5)] el maximo valor era 100

# ¿Por qué se trata de un algoritmo Greedy?
# Porque toma una decision basado en un maximo local para llegar a un maximo global
# En este caso, tomar primero el elemento con mayor relación valor/peso para maximizar la utilización del espacio

def mochila(elementos, W):
    elementos.sort(key=lambda e: e[0]/e[1], reverse=True) # O(n log n)
    mochila = []
    for elemento in elementos: # O(n)
        if elemento[1] <= W:
            mochila.append(elemento)
            W -= elemento[1]
    return mochila









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