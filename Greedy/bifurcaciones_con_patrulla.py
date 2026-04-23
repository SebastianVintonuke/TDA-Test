# Complejidad: O(n log n), el termino dominante es el ordenamiento

# Justificar que la solución es óptima
# Demostración por inducción:
# Caso Base: 1 ciudad, se coloca la vigilancia en esa intersección, la solución es óptima
# Paso Inductivo: Tomo por hipótesis que mi algoritmo da la solución óptima para n ciudades.
# Para (n+1) ciudades:
# Si la ciudad (n+1) no está vigilada:
#   Siendo k la posición de (n+1) en el arreglo ordenado de ciudades las vigilancias previas a k no serán modificadas.
#
# * Antes un área de vigilancia empezaba en la ciudad que ahora es (k+1), pero ahora debe empezar en k para poder cubrirla,
#   si la última ciudad cubierta por esta vigilancia, llamémosla j, continua cubierta, no se necesitan vigilancias extras
#   Si la última ciudad cubierta por esta vigilancia, ya no está cubierta, la siguiente vigilancia debera empezar en esta,
#   Repetir desde '*' con k = j
#   es decir, se necesitarán la misma cantidad de vigilancias o a lo sumo una extra
#
# Si la ciudad (n+1) ya está vigilada:
#   La solución es la misma que para n, y por hipótesis esta es óptima

# ¿Por qué se trata de un algoritmo Greedy?
# Porque toma una decision en base a un óptimo local para llegar a un óptimo global,
# en este caso, poner la vigilancia en el punto más lejano posible, con respecto al primero sin vigilancia
# de forma que este quede vigilado y se cubra la mayor área posible, reduciendo la cantidad total de patrulleros utilizados
def bifurcaciones_con_patrulla(ciudades):
    ciudades.sort(key=lambda x: x[1]) # O(n log n)
    vigilancia = []

    indice = 0
    fin = len(ciudades)
    while indice < fin: # O(n)
        vigilancia_optima = ciudades[indice][1] + 50

        # Avanzo el índice hasta que me paso del punto óptimo
        while indice < fin and ciudades[indice][1] <= vigilancia_optima:
            indice += 1

        # Vigilo en la primera antes de pasarme
        vigilada = ciudades[indice - 1]
        vigilancia.append(vigilada)
        hasta_donde_vigilo = vigilada[1] + 50

        # Avanzo todas las que ahora están vigiladas
        while indice < fin and ciudades[indice][1] <= hasta_donde_vigilo:
            indice += 1

    return vigilancia





def test_patrullas():
    # Convertimos los kilómetros en tuplas (Nombre, Km) para que coincidan con tu algoritmo
    casos = [
        {"input": [100], "expected_count": 1, "desc": "Único pueblo"},
        {"input": [10, 20, 30, 40, 50, 60], "expected_count": 1, "desc": "Rango compacto"},
        {"input": [100, 150, 200], "expected_count": 1, "desc": "Límite exacto 50km"},
        {"input": [100, 200, 300], "expected_count": 3, "desc": "Muy dispersos"},
        {"input": [156, 185, 194, 242, 270], "expected_count": 2, "desc": "Caso del enunciado"},
        {"input": [10, 60, 110, 160], "expected_count": 2, "desc": "Encadenados"}
    ]

    for i, caso in enumerate(casos):
        # Transformamos la lista de km en lista de tuplas para el algoritmo
        ciudades_input = [(f"Ciudad_{km}", km) for km in caso["input"]]

        resultado = bifurcaciones_con_patrulla(ciudades_input)

        # 1. Verificar cantidad de patrullas
        count_ok = len(resultado) == caso["expected_count"]

        # 2. Verificar cobertura
        # resultado es una lista de tuplas, extraemos solo los km para validar
        km_patrullas = [p[1] for p in resultado]
        cobertura_ok = True
        for km_pueblo in caso["input"]:
            cubierto = any(abs(km_pueblo - kp) <= 50 for kp in km_patrullas)
            if not cubierto:
                cobertura_ok = False
                break

        # 3. Verificar que las patrullas estén en bifurcaciones reales (tuplas originales)
        ubicacion_ok = all(p in ciudades_input for p in resultado)

        if count_ok and cobertura_ok and ubicacion_ok:
            print(f"Test {i + 1} ({caso['desc']}): PASSED ✅")
        else:
            print(f"Test {i + 1} ({caso['desc']}): FAILED ❌")
            if not count_ok:
                print(f"   Cant. patrullas incorrecta: {len(resultado)} (esperaba {caso['expected_count']})")
            if not cobertura_ok:
                print(f"   Hay pueblos sin cobertura a 50km.")
            if not ubicacion_ok:
                print(f"   Error: El patrullero no es una de las tuplas originales.")


if __name__ == '__main__':
    test_patrullas()