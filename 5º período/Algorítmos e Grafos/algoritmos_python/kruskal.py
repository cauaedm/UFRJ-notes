# Implementação de Kruskal
class Subconjunto:
    def __init__(self, pai, rank):
        self.pai = pai
        self.rank = rank

def encontrar(subs, i):
    if subs[i].pai != i:
        subs[i].pai = encontrar(subs, subs[i].pai)
    return subs[i].pai

def unir(subs, x, y):
    xraiz = encontrar(subs, x)
    yraiz = encontrar(subs, y)
    if subs[xraiz].rank < subs[yraiz].rank:
        subs[xraiz].pai = yraiz
    elif subs[xraiz].rank > subs[yraiz].rank:
        subs[yraiz].pai = xraiz
    else:
        subs[yraiz].pai = xraiz
        subs[xraiz].rank += 1

def kruskal(vertices, arestas):
    arestas = sorted(arestas, key=lambda x: x[2])
    subs = [Subconjunto(i, 0) for i in range(vertices)]
    mst = []
    for u, v, peso in arestas:
        x = encontrar(subs, u)
        y = encontrar(subs, v)
        if x != y:
            mst.append((u, v, peso))
            unir(subs, x, y)
    return mst

# Exemplo de uso:
# vertices = 4
# arestas = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
# print(kruskal(vertices, arestas))
