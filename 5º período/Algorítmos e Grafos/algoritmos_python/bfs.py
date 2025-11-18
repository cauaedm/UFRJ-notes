# Implementação de BFS (Busca em Largura)
def bfs(grafo, inicio):
    visitados = set()
    fila = [inicio]
    ordem = []
    while fila:
        vertice = fila.pop(0)
        if vertice not in visitados:
            visitados.add(vertice)
            ordem.append(vertice)
            fila.extend([viz for viz in grafo[vertice] if viz not in visitados])
    return ordem

# Exemplo de uso:
# grafo = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'], 'D': ['B'], 'E': ['B', 'F'], 'F': ['C', 'E']}
# print(bfs(grafo, 'A'))
