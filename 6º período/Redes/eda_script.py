import pandas as pd
import numpy as np
import ast

def parse_rtts(rtt_str):
    try:
        return ast.literal_eval(rtt_str)
    except:
        return []

def main():
    print("Carregando dados...")
    df = pd.read_csv('train.csv')
    
    print(f"Shape: {df.shape}")
    print("\nInfo:")
    print(df.info())
    
    print("\nDistribuição do target:")
    print(df['route_changed'].value_counts(normalize=True))
    
    print("\nValores faltantes:")
    print(df.isnull().sum())
    
    print("\nEstatísticas:")
    print(df.describe())
    
    print("\nParsing 'all_rtts'...")
    df['rtts_parsed'] = df['all_rtts'].apply(parse_rtts)
    df['avg_rtt'] = df['rtts_parsed'].apply(lambda x: np.mean(x) if x else np.nan)
    print(df[['all_rtts', 'avg_rtt']].head())

if __name__ == "__main__":
    main()
