
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Algorítmos e Grafos')))
from algoritmos_python.dijkstra import dijkstra
from algoritmos_python.kruskal import kruskal
from algoritmos_python.floyd_warshall import floyd_warshall
from algoritmos_python.componentes_conexas import componentes_conexas
from algoritmos_python.bfs import bfs
from algoritmos_python.dfs import dfs

# Funções de análise

def caminho_mais_curto(grafo, bairros, origem, destino):
    dist = dijkstra(grafo, origem)
    return dist[destino]

def arvore_geradora_minima(bairros, ruas):
    return kruskal(len(bairros), ruas)

def todas_distancias(grafo):
    return floyd_warshall(grafo)

def regioes_desconectadas(grafo):
    return componentes_conexas(grafo)

def busca_largura(grafo, inicio):
    return bfs(grafo, inicio)

def busca_profundidade(grafo, inicio):
    return dfs(grafo, inicio)
