import copy


class vertex:
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.distance = -1
        self.predecessor = None


class digraph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, value):
        if value not in self.vertices:
            self.vertices[value] = vertex(value)
        return self.vertices[value]

    def add_edge(self, from_vertex, to_vertex, capacity, flow=0):
        if from_vertex not in self.vertices:
            self.add_vertex(from_vertex)
        if to_vertex not in self.vertices:
            self.add_vertex(to_vertex)
        self.vertices[from_vertex].edges.append((to_vertex, flow, capacity))

    def remove_edge(self, from_vertex, to_vertex):
        for edge in self.vertices[from_vertex].edges:
            if edge[0] == to_vertex:
                self.vertices[from_vertex].edges.remove(edge)
                break

    def has_edge(self, from_vertex, to_vertex):
        for edge in self.vertices[from_vertex].edges:
            if edge[0] == to_vertex:
                return True
        return False

    def find_edge(self, from_vertex, to_vertex):
        for edge in self.vertices[from_vertex].edges:
            if edge[0] == to_vertex:
                return edge
        return None

    def update_edge(self, source, sink, flow):
        edge = self.find_edge(source, sink)
        edge = (edge[0], edge[1] + flow, edge[2])
        self.remove_edge(source, sink)
        self.add_edge(source, sink, edge[2], flow=edge[1])

    def set_predecessor(self, vertex, predecessor):
        vertex = self.vertices[vertex]
        vertex.predecessor = predecessor

    def BFS(self, node):
        visited = []
        queue = []
        node = self.vertices[node]
        visited.append(node)
        queue.append(node)

        while queue:
            m = queue.pop(0)
            for edge in m.edges:
                vertex = self.vertices[edge[0]]
                if vertex not in visited:
                    vertex.distance = m.distance + 1
                    vertex.predecessor = m
                    visited.append(vertex)
                    queue.append(vertex)

    def backtrack(self, node):
        node = self.vertices[node]
        path = []
        while node.predecessor:
            path.append(node.value)
            node = node.predecessor
        path.append(node.value)
        return path[::-1]

    def bottleneck(self, path):
        bottleneck = float('inf')
        for i in range(len(path) - 1):
            edge = self.find_edge(path[i], path[i + 1])
            if (edge is None):
                return -1
            bottleneck = min(bottleneck, edge[2])
        return bottleneck

    def residual_network(self, path):
        for i in range(len(path) - 1):
            origin = path[i]
            dest, flow, capacity = copy.deepcopy(
                self.find_edge(path[i], path[i + 1]))

            self.remove_edge(origin, dest)

            if(self.has_edge(dest, origin)):
                _, _flow, _capacity = self.find_edge(dest, origin)
                self.remove_edge(dest, origin)
                self.add_edge(dest, origin, flow+_capacity, flow=_flow)
            else:
                self.add_edge(dest, origin, flow, flow=flow)

            if(capacity != flow):
                self.add_edge(origin, dest, capacity - flow, flow=0)

    def edmonds_karp(self, source, sink):
        f = 0
        residual = self.copy_graph()
        while True:
            residual.BFS(source)

            path = residual.backtrack(sink)
            if(path[0] != source):
                return f

            bottleneck = residual.bottleneck(path)
            if(bottleneck == -1):
                return f
            f += bottleneck

            for i in range(len(path) - 1):
                edge = residual.find_edge(path[i], path[i + 1])
                edge = (edge[0], edge[1] + bottleneck, edge[2])
                residual.update_edge(path[i], path[i + 1], edge[1])

                origin = path[i]
                edge = self.find_edge(path[i], path[i+1])
                if(edge is not None):
                    _dest, _flow, _capacity = edge
                    self.remove_edge(origin, _dest)
                    self.add_edge(origin, _dest, _capacity,
                                  flow=_flow + bottleneck)
                edge = self.find_edge(path[i+1], path[i])

            residual.residual_network(path)

    def print_graph(self):
        for vertex in self.vertices:
            print(vertex, self.vertices[vertex].edges)

    def copy_graph(self):
        graph = digraph()
        for vertex in self.vertices:
            graph.add_vertex(vertex)
            for edge in self.vertices[vertex].edges:
                graph.add_edge(vertex, edge[0], edge[2], flow=edge[1])
        return graph

    def pair_check(self):
        pairs = self.vertices['s'].edges
        passed = set()
        # Percorrendo os pares (programa - programa vizinho)
        for pair in pairs:
            edge1, edge2 = self.vertices[pair[0]].edges

            # Dado que o (programa - programa vizinho) é um par (x - y)
            # Verificando as arestas do programa x e o programa y que estao incidindo em t
            _dest1, _flow1, _capacity1 = self.find_edge(edge1[0], 't')
            _dest2, _flow2, _capacity2 = self.find_edge(edge2[0], 't')

            # Caso o programa x e o programa y utilizaram 100% da sua capacidade
            # Ou seja, o lucro é >= custo, então o par (x, y) é valido
            # pois vale a pena implementar o programa x e o programa y
            if(_flow1 == _capacity1 and _flow2 == _capacity2):
                passed.add(edge1[0])
                passed.add(edge2[0])

        return passed

# A entrada é um grafo não-dirigido com pesos nos vértices
# O peso é acessado pelo atributo "peso" e os vizinhos pelo atributo "vizinhos"
# Para cada vizinho, existe uma tupla (x,y), onde x é o nome do vizinho e y é o peso da aresta
# Cada vértice representa um programa


def EXERCICIO_3(entrada):
    dg = digraph()
    # Adicionando os vértices inicial e final
    dg.add_vertex("s")
    dg.add_vertex("t")

    # Percorrendo a entrada
    for v in entrada:
        v = dict(v)

        key = list(v.keys())[0]  # Nome do vértice
        value = v[key]  # Peso + Vizinhos

        peso = value["peso"]  # Retornando o peso

        dg.add_vertex(key)  # Adicionando o vértice programa
        # Ligando o programa ao final com seu peso em valor absoluto (custo)
        dg.add_edge(key, "t", abs(peso))

        # Percorrendo os vizinhos (caso existam)
        if("vizinhos" in value):
            vizinhos = value["vizinhos"]  # Retornando os vizinhos
            for vizinho in vizinhos:  # Percorrendo os vizinhos
                nome, peso = vizinho  # Retornando o nome e o peso do vizinho
                # Criando o par (programa - programa vizinho)
                pair = key + '-' + nome
                dg.add_vertex(pair)  # Adicionando o par

                # Ligando o par ao início com seu peso (lucro)
                dg.add_edge("s", pair, peso)
                # Ligando o par ao programa
                dg.add_edge(pair, key, float('inf'))
                # Ligando o par ao programa vizinho
                dg.add_edge(pair, nome, float('inf'))

    # Calculando o fluxo máximo
    f = dg.edmonds_karp("s", "t")

    # Verificando e retornando os pares que satisfazem a condição
    print("Programas a serem portados: ")
    print(list(dg.pair_check()))


# A entrada conforme especificado
entrada = [
    {"1": {"peso": -8, "vizinhos": [("4", 5), ("3", 10)]}},
    {"2": {"peso": -6, "vizinhos": [("1", 4), ("3", 6)]}},
    {"3": {"peso": -2, "vizinhos": [("4", 3)]}},
    {"4": {"peso": -4}}
]

EXERCICIO_3(entrada)