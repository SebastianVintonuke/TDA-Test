
def parte_entera_raiz(n) -> int:
    return parte_entera_raiz_db(n, 0, n)

# Complejidad: O(log(n)
# Teorema Maestro, A = 1, B = 2, C = 0
# Log2(1) = 1 > 0 => n ^ 0 * log2(n) = log(n)
def parte_entera_raiz_db(n, inicio, fin):
    if fin - inicio == 0:
        return inicio
    else:
        centro = (inicio + fin) // 2

        candidato_1 = centro * centro
        candidato_2 = (centro + 1) * (centro + 1)
        if candidato_1 == n or (candidato_1 < n < candidato_2):
            return centro

        if candidato_1 > n:
            return parte_entera_raiz_db(n, inicio, centro)
        else:
            return parte_entera_raiz_db(n, centro + 1, fin)











def test_raiz_entera(func):
    """
    Suite de pruebas para validar la función de raíz cuadrada entera.
    Se espera que 'func' sea el nombre de tu función.
    """
    test_cases = [
        # (n, resultado_esperado)
        (0, 0),       # Caso base: cero
        (1, 1),       # Caso base: uno
        (2, 1),       # Raíz de 2 es ~1.41 -> 1
        (3, 1),       # Raíz de 3 es ~1.73 -> 1
        (4, 2),       # Cuadrado perfecto
        (8, 2),       # Raíz de 8 es ~2.82 -> 2
        (9, 3),       # Cuadrado perfecto
        (10, 3),      # Ejemplo del enunciado
        (15, 3),      # Justo antes de 16
        (16, 4),      # Cuadrado perfecto
        (24, 4),      # Justo antes de 25
        (25, 5),      # Ejemplo del enunciado
        (99, 9),      # Justo antes de 100
        (100, 10),    # Cuadrado perfecto
        (101, 10),    # Justo después de 100
        (1000, 31),   # 31^2 = 961, 32^2 = 1024
        (2147483647, 46340), # Límite superior de entero de 32 bits
    ]

    success = True
    for n, expected in test_cases:
        try:
            result = func(n)
            assert result == expected, f"❌ Fallo en n={n}: se esperaba {expected}, se obtuvo {result}"
        except Exception as e:
            print(f"💥 Error al ejecutar n={n}: {e}")
            success = False
            continue

    if success:
        print("✅ ¡Todas las pruebas pasaron exitosamente!")

test_raiz_entera(parte_entera_raiz)