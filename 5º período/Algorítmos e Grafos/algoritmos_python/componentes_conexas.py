# Implementação de busca de componentes conexas (algoritmo de Tarjan, também chamado de Caravajo em alguns contextos)
def componentes_conexas(grafo):
    visitados = set()
    componentes = []
    def dfs(v, comp):
        visitados.add(v)
        comp.append(v)
        for viz in grafo[v]:
            if viz not in visitados:
                dfs(viz, comp)
    for v in grafo:
        if v not in visitados:
            comp = []
            dfs(v, comp)
            componentes.append(comp)
    return componentes

# Exemplo de uso:
# grafo = {'A': ['B'], 'B': ['A'], 'C': ['D'], 'D': ['C'], 'E': []}
# print(componentes_conexas(grafo))
