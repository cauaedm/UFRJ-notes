import pandas as pd
import numpy as np
import time

def bench_rtt():
    # Cria dados de teste com listas de RTT
    N = 100000
    print(f"Criando {N} linhas dummy...")
    df = pd.DataFrame({'rtts': [[10.5, 20.1, 15.3] for _ in range(N)]})
    
    # Método mais lento: aplica função em cada linha
    print("Método 1: Apply")
    start = time.time()
    def get_stats(rtt_list):
        if not rtt_list:
            return pd.Series([np.nan]*4)
        return pd.Series([np.mean(rtt_list), np.std(rtt_list), np.min(rtt_list), np.max(rtt_list)])
    
    _ = df['rtts'].apply(get_stats)
    print(f"Tempo: {time.time() - start:.4f}s")
    
    # Método vetorizado: expande lista em colunas e calcula de uma vez
    print("Método 2: Expansão Vetorizada")
    start = time.time()
    expanded = pd.DataFrame(df['rtts'].tolist())
    
    mean = expanded.mean(axis=1)
    std = expanded.std(axis=1)
    min_ = expanded.min(axis=1)
    max_ = expanded.max(axis=1)
    print(f"Tempo: {time.time() - start:.4f}s")

if __name__ == "__main__":
    bench_rtt()
