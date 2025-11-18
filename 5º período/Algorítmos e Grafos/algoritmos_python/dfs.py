# Implementação de DFS (Busca em Profundidade)
def dfs(grafo, inicio, visitados=None, ordem=None):
    if visitados is None:
        visitados = set()
    if ordem is None:
        ordem = []
    visitados.add(inicio)
    ordem.append(inicio)
    for vizinho in grafo[inicio]:
        if vizinho not in visitados:
            dfs(grafo, vizinho, visitados, ordem)
    return ordem

# Exemplo de uso:
# grafo = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'], 'D': ['B'], 'E': ['B', 'F'], 'F': ['C', 'E']}
# print(dfs(grafo, 'A'))
