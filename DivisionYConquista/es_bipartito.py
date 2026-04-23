
import random

class Grafo:
    def __init__(self):
        self.grafo = {}

    # Recibe un vertice valido y devuelve un bool.
    # Crea dicho vertice.
    def agregar_vertice(self, vertice):
        if self.existe(vertice):
            return False
        self.grafo[vertice] = {}
        return True

    # Recibe 2 vertices validos, un peso y devuelve un bool.
    # Crea una arista entre dos vertices, si ya existe, actualiza su peso.
    def agregar_arista(self, vertice1, vertice2, peso):
        if not self.existe(vertice1) or not self.existe(vertice2):
            return False
        self.grafo[vertice1][vertice2] = peso
        self.grafo[vertice2][vertice1] = peso
        return True
    
    # Recibe un vertice y devuelve un bool.
    # Si el vertice esta en el grafo devuelve True, si no, devuelve False.
    def existe(self, vertice):
        return vertice in self.grafo
    
    # Itera todos los vértices del grafo en un orden aleatorio.
    def __iter__(self):
        vertices = list(self.grafo.keys())
        random.shuffle(vertices)  # mezclamos los vértices
        return iter(vertices)
    
    # Recibe 2 vertices validos y devuelve un bool
    # Si ambos vertices son adyacentes devuelve True, si no devuelve False.
    def hay_arista(self, origen, destino) -> bool:
        if not self.existe(origen) or not self.existe(destino):
            return False
        return destino in self.grafo[origen]

    # Recibe un vertice valido
    # Si existe el vertice devuelve un array con los vertices adyacentes, si no, devuelve None.
    def adyacentes(self, vertice) -> list | None:
        if not self.existe(vertice):
            return None
        return list(self.grafo[vertice].keys())
    
    # Devuelve un array con los vertices del grafo.
    def vertices(self) -> list:
        return list(self.grafo.keys())

"""
def es_bipartito(grafo: Grafo) -> bool:
    if not grafo.vertices():
        return True

    origen = grafo.vertices()[0]

    rojo = set()
    azul = set()
    rojo.add(origen)

    a_visitar_vecinos = []
    a_visitar_vecinos.append(origen)
    while a_visitar_vecinos:
        visitado = a_visitar_vecinos.pop(0)
        for vecino in grafo.adyacentes(visitado):

            if visitado in rojo:
                if vecino in rojo:
                    return False
                elif vecino not in azul:
                    azul.add(vecino)
                    a_visitar_vecinos.append(vecino)
            else:
                if vecino in azul:
                    return False
                elif vecino not in rojo:
                    rojo.add(vecino)
                    a_visitar_vecinos.append(vecino)
    return True
"""
    
def es_bipartito(grafo):
    componentes_conexas = set(grafo.vertices())

    visitados_con_color = {}
    vertices_con_vecinos_para_visitar = []

    while vertices_con_vecinos_para_visitar or componentes_conexas:
        if not vertices_con_vecinos_para_visitar:
            origen = componentes_conexas.pop()
            visitados_con_color[origen] = "rojo"
            vertices_con_vecinos_para_visitar.append(origen)

        visitado = vertices_con_vecinos_para_visitar.pop(0)
        color_del_visitado = visitados_con_color[visitado]
        color_opuesto = "azul" if color_del_visitado == "rojo" else "rojo"
    
        for vecino in grafo.adyacentes(visitado):
            if vecino not in visitados_con_color:
                visitados_con_color[vecino] = color_opuesto
                vertices_con_vecinos_para_visitar.append(vecino)
                componentes_conexas.remove(vecino)
            else:
                if visitados_con_color[vecino] == color_del_visitado:
                    return False             
    return True