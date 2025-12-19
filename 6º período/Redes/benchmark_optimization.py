import pandas as pd
import numpy as np
import time
import json

def bench():
    # Compara dois métodos de parsing de strings para listas
    print("Gerando dados (1M linhas)...")
    data = {'all_rtts': ['[12.5, 45.1, 33.2]'] * 1000000}
    df = pd.DataFrame(data)
    
    # Método usando JSON parser
    print("Método 1: Apply JSON...")
    start = time.time()
    _ = df['all_rtts'].apply(json.loads)
    print(f"Tempo: {time.time() - start:.4f}s")
    
    # Método usando operações de string vetorizadas
    print("Método 2: Split Vetorizado...")
    start = time.time()
    expanded = df['all_rtts'].str.strip('[]').str.split(',', expand=True).astype(float)
    _ = expanded.mean(axis=1)
    print(f"Tempo: {time.time() - start:.4f}s")

if __name__ == "__main__":
    bench()
