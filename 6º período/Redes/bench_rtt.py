import pandas as pd
import numpy as np
import time

def bench_rtt():
    N = 100000
    print(f"Creating {N} dummy rows...")
    # Simulate list of 3 floats
    df = pd.DataFrame({'rtts': [[10.5, 20.1, 15.3] for _ in range(N)]})
    
    print("Method 1: Apply (Current)")
    start = time.time()
    def get_stats(rtt_list):
        if not rtt_list:
            return pd.Series([np.nan]*4)
        return pd.Series([np.mean(rtt_list), np.std(rtt_list), np.min(rtt_list), np.max(rtt_list)])
    
    _ = df['rtts'].apply(get_stats)
    print(f"Time: {time.time() - start:.4f}s")
    
    print("Method 2: Vectorized Expansion")
    start = time.time()
    # Expand list to columns
    # This is usually much faster
    expanded = pd.DataFrame(df['rtts'].tolist())
    
    mean = expanded.mean(axis=1)
    std = expanded.std(axis=1)
    min_ = expanded.min(axis=1)
    max_ = expanded.max(axis=1)
    print(f"Time: {time.time() - start:.4f}s")

if __name__ == "__main__":
    bench_rtt()
