import pandas as pd
import numpy as np
import time
import json

def bench():
    # Create dummy large data
    print("Generating dummy data (1M rows)...")
    data = {'all_rtts': ['[12.5, 45.1, 33.2]'] * 1000000}
    df = pd.DataFrame(data)
    
    # Method 1: Apply JSON
    print("Benchmarking Method 1: Apply JSON/Eval...")
    start = time.time()
    _ = df['all_rtts'].apply(json.loads)
    print(f"Method 1 Time: {time.time() - start:.4f}s")
    
    # Method 2: Vectorized String Split
    print("Benchmarking Method 2: Vectorized String Split...")
    start = time.time()
    # Remove brackets, split by comma, expand to columns, convert to float
    expanded = df['all_rtts'].str.strip('[]').str.split(',', expand=True).astype(float)
    # Calcs
    _ = expanded.mean(axis=1)
    print(f"Method 2 Time: {time.time() - start:.4f}s")

if __name__ == "__main__":
    bench()
