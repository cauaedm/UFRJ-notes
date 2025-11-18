from grafo_transito import carregar_bairros, carregar_ruas, construir_grafo
from analises import caminho_mais_curto, arvore_geradora_minima, todas_distancias, regioes_desconectadas, busca_largura, busca_profundidade
import os

DADOS_DIR = os.path.join(os.path.dirname(__file__), 'dados')

bairros = carregar_bairros(os.path.join(DADOS_DIR, 'bairros.csv'))
ruas = carregar_ruas(os.path.join(DADOS_DIR, 'ruas.csv'))
grafo = construir_grafo(bairros, ruas)

print('Bairros:', bairros)
print('Exemplo de análise de trânsito com grafos:')

# 1. Caminho mais curto entre Centro e Leblon
origem, destino = 0, 3
print(f"Caminho mais curto de {bairros[origem]} até {bairros[destino]}: {caminho_mais_curto(grafo, bairros, origem, destino)} km")

# 2. Árvore geradora mínima (custo mínimo para conectar todos os bairros)
mst = arvore_geradora_minima(bairros, ruas)
print('Árvore geradora mínima (ruas selecionadas):')
for u, v, peso in mst:
    print(f"{bairros[u]} <-> {bairros[v]}: {peso} km")

# 3. Todas as distâncias entre bairros
distancias = todas_distancias(grafo)
print('Distâncias mínimas entre todos os bairros:')
for u in bairros:
    for v in bairros:
        if u != v:
            print(f"{bairros[u]} -> {bairros[v]}: {distancias[u][v]} km")

# 4. Componentes conexas (regiões desconectadas)
componentes = regioes_desconectadas(grafo)
print('Componentes conexas (regiões conectadas):')
for comp in componentes:
    print([bairros[v] for v in comp])

# 5. Busca em largura a partir do Centro
print('BFS a partir do Centro:', [bairros[v] for v in busca_largura(grafo, 0)])

# 6. Busca em profundidade a partir do Centro
print('DFS a partir do Centro:', [bairros[v] for v in busca_profundidade(grafo, 0)])
