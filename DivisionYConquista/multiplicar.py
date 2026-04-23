
# Complejidad: O(n ^ 1.58)
# Teorema Maestro, A = 3, B = 2, C = 1
# Log2(3) = 1.58 > C => n ^ log2(3) = n ^ 1.58
def multiplicar(a, b):
    if a < 255 or b < 255:
        return a * b

    largo_a = a.bit_length()
    largo_b = b.bit_length()
    max_largo = largo_a if largo_a > largo_b else largo_b
    n_sobre_base = max_largo // 2

    x0, x1 = separar_en_primera_mitad_y_segunda_mitad(a, n_sobre_base)
    y0, y1 = separar_en_primera_mitad_y_segunda_mitad(b, n_sobre_base)

    p = multiplicar(x1 + x0, y1 + y0)
    x1y1 = multiplicar(x1, y1)
    x0y0 = multiplicar(x0, y0)

    return (x1y1 * (2**(2 * n_sobre_base))) + ((p - x1y1 - x0y0) * (2 ** n_sobre_base)) + x0y0

# Complejidad: O(n)
def separar_en_primera_mitad_y_segunda_mitad(x, n_sobre_base):
    x1 = x >> n_sobre_base
    x0 = x & ((2**n_sobre_base) - 1)
    return (x0, x1)

def test_multiplicar():
    casos = [
        (5, 8),                # 1 dígito
        (12, 10),              # 2 dígitos
        (123, 456),            # 3 dígitos
        (1234, 5678),          # 4 dígitos
        (12345, 67890),        # 5 dígitos
        (123456, 987654),      # 6 dígitos
        (1234567, 1111111),    # 7 dígitos
        (12345678, 87654321),  # 8 dígitos
        (123456789, 987654321) # 9 dígitos
    ]

    print(f"{'Operación':<25} | {'Resultado Karatsuba':<20} | {'¿Correcto?':<10}")
    print("-" * 65)

    for a, b in casos:
        resultado_mio = multiplicar(a, b)
        resultado_real = a * b
        check = "✅" if resultado_mio == resultado_real else "❌"
        print(f"{a} * {b:<15} | {resultado_mio:<20} | {check}")

test_multiplicar()

