# Projeto: Análise de Rotas de Trânsito com Grafos

Este projeto demonstra a aplicação de algoritmos de grafos para análise de rotas de trânsito em uma cidade fictícia. Utiliza algoritmos clássicos (BFS, DFS, Dijkstra, Kruskal, Floyd-Warshall, Componentes Conexas) para responder perguntas reais sobre o trânsito, como:

- Qual o caminho mais curto entre dois pontos?
- Existem regiões desconectadas?
- Qual o custo mínimo para conectar todos os bairros?
- Como identificar congestionamentos e alternativas?

## Estrutura
- `grafo_transito.py`: Definição do grafo de trânsito (bairros, ruas, distâncias).
- `analises.py`: Funções de análise usando os algoritmos clássicos.
- `main.py`: Interface de execução e exemplos de análise.
- `dados/`: Pasta para mapas e dados de trânsito (exemplo: bairros.csv, ruas.csv).

## Como usar
1. Edite os arquivos em `dados/` para mapear sua cidade ou use os exemplos.
2. Execute `main.py` para ver exemplos de análise.

---

Este projeto pode ser expandido para cidades reais, integração com APIs de mapas, análise de tráfego em tempo real, etc.