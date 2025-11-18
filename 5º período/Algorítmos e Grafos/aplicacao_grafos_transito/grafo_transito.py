import csv

def carregar_bairros(caminho):
    bairros = {}
    with open(caminho, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bairros[int(row['bairro_id'])] = row['nome']
    return bairros

def carregar_ruas(caminho):
    ruas = []
    with open(caminho, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ruas.append((int(row['origem']), int(row['destino']), float(row['distancia'])))
    return ruas

def construir_grafo(bairros, ruas):
    grafo = {b: [] for b in bairros}
    for origem, destino, distancia in ruas:
        grafo[origem].append((destino, distancia))
        grafo[destino].append((origem, distancia))  # grafo não-direcionado
    return grafo
