# Implementação de Floyd-Warshall (Floyd-Fulkerson não é um algoritmo clássico, provavelmente quis dizer Floyd-Warshall)
def floyd_warshall(grafo):
    dist = {u: {v: float('inf') for v in grafo} for u in grafo}
    for u in grafo:
        dist[u][u] = 0
        for v, peso in grafo[u]:
            dist[u][v] = peso
    for k in grafo:
        for i in grafo:
            for j in grafo:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# Exemplo de uso:
# grafo = {'A': [('B', 3), ('C', 8)], 'B': [('C', 2), ('D', 5)], 'C': [('D', 1)], 'D': []}
# print(floyd_warshall(grafo))
