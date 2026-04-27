def plan_operativo(arreglo_L, arreglo_C, costo_M):
    optimos_l, optimos_c = c_optimos(arreglo_L, arreglo_C, costo_M)
    return c_solucion(arreglo_L, arreglo_C, costo_M, optimos_l, optimos_c)

def c_optimos(arreglo_L, arreglo_C, costo_M):
    n_meses = len(arreglo_L)
    optimos_l = [ 0 for _ in range(n_meses)]
    optimos_c = [ 0 for _ in range(n_meses)]

    optimos_l[0] = min(arreglo_L[0], arreglo_C[0] + costo_M)
    optimos_c[0] = min(arreglo_C[0], arreglo_L[0] + costo_M)

    for mes in range(1, len(arreglo_L)):
        optimos_l[mes] = min(optimos_l[mes - 1] + arreglo_L[mes], optimos_c[mes - 1] + costo_M + arreglo_L[mes])
        optimos_c[mes] = min(optimos_c[mes - 1] + arreglo_C[mes], optimos_l[mes - 1] + costo_M + arreglo_C[mes])

    return optimos_l, optimos_c

def c_solucion(arreglo_L, arreglo_C, costo_M, optimos_l, optimos_c):
    solucion = []
    n_meses = len(arreglo_L)
    mes = n_meses - 1

    if optimos_l[mes] < optimos_c[mes]:
        estoy_en = 'londres'
        solucion.append('londres')
    else:
        solucion.append('california')
        estoy_en = 'california'
    mes -= 1

    while mes >= 0:
        if estoy_en == 'londres':
            quedarme = optimos_l[mes-1] + arreglo_L[mes]
            mudarme = optimos_l[mes-1] + costo_M + arreglo_C[mes]
            if quedarme <= mudarme:
                solucion.append('londres')
            else:
                solucion.append('california')
                estoy_en = 'california'
        else:
            quedarme = optimos_c[mes-1] + arreglo_C[mes]
            mudarme = optimos_c[mes-1] + costo_M + arreglo_L[mes]
            if quedarme <= mudarme:
                solucion.append('california')
            else:
                solucion.append('londres')
                estoy_en = 'londres'
        mes -= 1

    solucion.reverse()
    return solucion








import unittest

class TestPlanOperativo(unittest.TestCase):

    def test_un_solo_mes(self):
        # Caso base: un solo mes, debe elegir el más barato
        self.assertEqual(plan_operativo([10], [20], 50), ["londres"])
        self.assertEqual(plan_operativo([30], [10], 50), ["california"])

    def test_mudanza_cara_no_conviene(self):
        # Aunque california es más barato el segundo mes, la mudanza M=100 lo hace inviable
        L = [10, 50]
        C = [40, 40]
        M = 100
        # Es mejor quedarse en londres: total 60 vs (40+100+40=180)
        self.assertEqual(plan_operativo(L, C, M), ["londres", "londres"])

    def test_mudanza_barata_conviene(self):
        # M es muy bajo, conviene ir rotando a la ciudad más barata
        L = [10, 100, 10]
        C = [100, 10, 100]
        M = 5
        # Total: 10 (L) + 5 (M) + 10 (C) + 5 (M) + 10 (L) = 40
        self.assertEqual(plan_operativo(L, C, M), ["londres", "california", "londres"])

    def test_empieza_en_california(self):
        # El primer mes dicta el inicio
        L = [100, 100]
        C = [10, 10]
        M = 50
        self.assertEqual(plan_operativo(L, C, M), ["california", "california"])

    def test_costos_iguales(self):
        # Si son iguales, cualquier camino es válido, pero no debería haber mudanzas innecesarias
        L = [10, 10, 10]
        C = [10, 10, 10]
        M = 5
        resultado = plan_operativo(L, C, M)
        # Verificamos que se quede en una sola ciudad (la que elija el algoritmo por defecto)
        self.assertTrue(all(x == resultado[0] for x in resultado))

    def test_cambio_al_final(self):
        # Conviene mudarse solo en el último mes
        L = [10, 10, 100]
        C = [50, 50, 10]
        M = 20
        # londres (10) + londres (10) + Mudanza (20) + california (10) = 50
        # Quedarse siempre en londres = 120
        self.assertEqual(plan_operativo(L, C, M), ["londres", "londres", "california"])

    def test_n_grande_consistencia(self):
        # Prueba de longitud para asegurar que devuelve n elementos
        n = 100
        L = [10] * n
        C = [10] * n
        M = 5
        resultado = plan_operativo(L, C, M)
        self.assertEqual(len(resultado), n)

if __name__ == '__main__':
    unittest.main()
