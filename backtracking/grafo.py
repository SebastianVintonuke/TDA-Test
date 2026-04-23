import random

class Grafo:
    def __init__(self, dirigido=False, vertices_init=[]):
        """
        Inicializa un grafo.
        Si dirigido es False, las aristas son bidireccionales.
        """
        self.dirigido = dirigido
        self.vertices = {}
        for v in vertices_init:
            self.agregar_vertice(v)

    def agregar_vertice(self, v):
        """Agrega un vértice al grafo si no existe."""
        if v not in self.vertices:
            self.vertices[v] = {}

    def borrar_vertice(self, v):
        """Elimina el vértice y todas las aristas asociadas a él."""
        if v in self.vertices:
            # Eliminar el vértice
            del self.vertices[v]
            # Eliminar referencias de otros vértices hacia este
            for u in self.vertices:
                if v in self.vertices[u]:
                    del self.vertices[u][v]

    def agregar_arista(self, v, w, peso=1):
        """
        Agrega una arista entre v y w.
        Si el grafo no es dirigido, crea la conexión v <--> w.
        """
        if v not in self.vertices: self.agregar_vertice(v)
        if w not in self.vertices: self.agregar_vertice(w)

        self.vertices[v][w] = peso
        if not self.dirigido:
            self.vertices[w][v] = peso

    def borrar_arista(self, v, w):
        """Borra la arista entre v y w."""
        if v in self.vertices and w in self.vertices[v]:
            del self.vertices[v][w]
            if not self.dirigido and w in self.vertices and v in self.vertices[w]:
                del self.vertices[w][v]

    def estan_unidos(self, v, w):
        """Devuelve True si existe una arista de v a w."""
        return v in self.vertices and w in self.vertices[v]

    def peso_arista(self, v, w):
        """Devuelve el peso de la arista (v, w)."""
        if self.estan_unidos(v, w):
            return self.vertices[v][w]
        return None

    def obtener_vertices(self):
        """Devuelve una lista con todos los vértices del grafo."""
        return list(self.vertices.keys())

    def vertice_aleatorio(self):
        """Devuelve un vértice al azar del grafo."""
        if not self.vertices:
            return None
        return random.choice(list(self.vertices.keys()))

    def adyacentes(self, v):
        """Devuelve una lista con los vértices adyacentes a v."""
        if v in self.vertices:
            return list(self.vertices[v].keys())
        return []

    def __str__(self):
        """Representación en cadena del grafo."""
        return str(self.vertices)