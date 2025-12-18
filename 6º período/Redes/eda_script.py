import pandas as pd
import numpy as np
import ast

def parse_rtts(rtt_str):
    try:
        return ast.literal_eval(rtt_str)
    except:
        return []

def main():
    print("Loading data...")
    df = pd.read_csv('train.csv')
    
    print(f"Dataset Shape: {df.shape}")
    print("\nColumn Info:")
    print(df.info())
    
    print("\nTarget Distribution (route_changed):")
    print(df['route_changed'].value_counts(normalize=True))
    
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    print("\nNumerical Stats:")
    print(df.describe())
    
    # Sample parse of all_rtts
    print("\nParsing 'all_rtts' sample...")
    df['rtts_parsed'] = df['all_rtts'].apply(parse_rtts)
    df['avg_rtt'] = df['rtts_parsed'].apply(lambda x: np.mean(x) if x else np.nan)
    print(df[['all_rtts', 'avg_rtt']].head())

if __name__ == "__main__":
    main()
