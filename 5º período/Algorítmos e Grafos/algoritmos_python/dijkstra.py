# Implementação de Dijkstra
import heapq

def dijkstra(grafo, inicio):
    dist = {v: float('inf') for v in grafo}
    dist[inicio] = 0
    heap = [(0, inicio)]
    while heap:
        custo, u = heapq.heappop(heap)
        if custo > dist[u]:
            continue
        for v, peso in grafo[u]:
            if dist[v] > dist[u] + peso:
                dist[v] = dist[u] + peso
                heapq.heappush(heap, (dist[v], v))
    return dist

# Exemplo de uso:
# grafo = {'A': [('B', 1), ('C', 4)], 'B': [('A', 1), ('C', 2), ('D', 5)], 'C': [('A', 4), ('B', 2), ('D', 1)], 'D': [('B', 5), ('C', 1)]}
# print(dijkstra(grafo, 'A'))
