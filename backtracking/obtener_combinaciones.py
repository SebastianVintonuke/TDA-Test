def obtener_combinaciones(materias):
    combinaciones = []
    for materia in materias:
        for curso in materia:
            materias_restantes = [ m for m in materias if m != materia ]
            resultado = obtener_combinaciones_rec(materias_restantes, [curso])
            if resultado:
                combinaciones.append(resultado)
                break
    return combinaciones

def obtener_combinaciones_rec(materias, cursos_tomados):
    if not materias:
        return cursos_tomados

    materia_actual = materias.pop()
    for curso_candidato in materia_actual:
        if all(son_compatibles(curso_candidato, curso) for curso in cursos_tomados):
            cursos_tomados.append(curso_candidato)
            resultado = obtener_combinaciones_rec(materias, cursos_tomados)
            if resultado:
                return resultado
            cursos_tomados.remove(curso_candidato)
    materias.append(materia_actual)
    return None
















import unittest


def son_compatibles(curso_1, curso_2):
    """
    Determina si dos cursos son compatibles.
    Cada curso es un diccionario con la clave 'horarios' (set de tuplas).
    """
    return curso_1['horarios'].isdisjoint(curso_2['horarios'])

class TestCombinacionesMaterias(unittest.TestCase):

    def test_una_materia_un_curso(self):
        """Una sola materia con un solo curso debería devolver una combinación."""
        m1_c1 = {'nombre': 'M1_C1', 'horarios': {('Lun', 9)}}
        materias = [[m1_c1]]

        resultado = obtener_combinaciones(materias)
        # Se espera una lista con una única combinación: [m1_c1]
        self.assertEqual(len(resultado), 1)
        self.assertIn(m1_c1, resultado[0])

    def test_dos_materias_compatibles(self):
        """Dos materias con cursos en horarios distintos."""
        m1_c1 = {'nombre': 'M1_C1', 'horarios': {('Lun', 9)}}
        m2_c1 = {'nombre': 'M2_C1', 'horarios': {('Mar', 9)}}
        materias = [[m1_c1], [m2_c1]]

        resultado = obtener_combinaciones(materias)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(len(resultado[0]), 2)

    def test_cursos_incompatibles(self):
        """Dos materias que solo tienen cursos que se solapan no deben dar resultados."""
        m1_c1 = {'nombre': 'M1_C1', 'horarios': {('Lun', 9), ('Lun', 10)}}
        m2_c1 = {'nombre': 'M2_C1', 'horarios': {('Lun', 10), ('Lun', 11)}}
        materias = [[m1_c1], [m2_c1]]

        resultado = obtener_combinaciones(materias)
        self.assertEqual(len(resultado), 0)

    def test_multiples_opciones_validas(self):
        """Debe encontrar todas las combinaciones que no se solapan."""
        # Materia 1 tiene 2 opciones
        m1_c1 = {'nombre': 'M1_C1', 'horarios': {('Lun', 9)}}
        m1_c2 = {'nombre': 'M1_C2', 'horarios': {('Mar', 9)}}
        # Materia 2 tiene 1 opción que solapa con M1_C1
        m2_c1 = {'nombre': 'M2_C1', 'horarios': {('Lun', 9)}}

        materias = [[m1_c1, m1_c2], [m2_c1]]

        resultado = obtener_combinaciones(materias)
        # Solo la combinación [M1_C2, M2_C1] es válida
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][0]['nombre'], 'M1_C2')

    def test_materia_sin_cursos(self):
        """Si una de las materias no tiene cursos, no hay combinación posible."""
        m1_c1 = {'nombre': 'M1_C1', 'horarios': {('Lun', 9)}}
        materias = [[m1_c1], []]

        resultado = obtener_combinaciones(materias)
        self.assertEqual(len(resultado), 0)


if __name__ == '__main__':
    unittest.main()