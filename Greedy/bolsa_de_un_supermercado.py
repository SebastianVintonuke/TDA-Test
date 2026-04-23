
# Complejidad O(n^2), en el peor caso cada producto va en una bolsa diferente, pero igual tengo que revisar todos para ver si alguno entra
# Para cada producto, reviso todos los productos

# ¿Es óptimo?
# Para cada bolsa intento meter tantos productos como pueda priorizando lo más grande,
# esto minimiza la cantidad de bolsas, ya que optimiza el uso de cada una
def bolsas(capacidad, productos):
    productos_ordenados = sorted(productos, reverse=False)
    resultado = []
    while productos_ordenados:
        productos_que_no_entran = []
        bolsa = []
        capacidad_bolsa = capacidad

        for producto in productos_ordenados:
            if capacidad_bolsa - producto >= 0:
                bolsa.append(producto)
                capacidad_bolsa -= producto
            else:
                productos_que_no_entran.append(producto)

        productos_ordenados = productos_que_no_entran
        resultado.append(bolsa)

    return resultado




def test_bolsas():
    # Test 1: ejemplo del enunciado
    productos = [4, 2, 1, 3, 5]
    capacidad = 5
    resultado = bolsas(capacidad, productos)
    # Verifica que cada bolsa no supere la capacidad
    assert all(sum(b) <= capacidad for b in resultado), "Error: bolsa excede la capacidad"
    # Verifica que se incluyan todos los productos
    assert sorted([p for bolsa in resultado for p in bolsa]) == sorted(productos), "Error: faltan productos"
    # Test simple de conteo mínimo posible (para este caso óptimo son 3 bolsas)
    assert len(resultado) == 3, f"Error: se esperaba 3 bolsas, se obtuvieron {len(resultado)}"

    # Test 2: productos que caben exactamente en una bolsa
    productos = [2, 3]
    capacidad = 5
    resultado = bolsas(capacidad, productos)
    assert len(resultado) == 1, f"Error: se esperaba 1 bolsa, se obtuvieron {len(resultado)}"

    # Test 3: productos más pequeños que la capacidad pero que requieren varias bolsas
    productos = [1, 1, 1, 1, 1, 1]
    capacidad = 3
    resultado = bolsas(capacidad, productos)
    # Cada bolsa puede contener hasta 3 elementos, deberían ser 2 bolsas
    assert len(resultado) == 2, f"Error: se esperaba 2 bolsas, se obtuvieron {len(resultado)}"

    # Test 5: lista vacía
    productos = []
    capacidad = 5
    resultado = bolsas(capacidad, productos)
    assert resultado == [], "Error: lista vacía debería devolver lista vacía de bolsas"

    print("Todos los tests pasaron correctamente.")

if __name__ == '__main__':
    test_bolsas()