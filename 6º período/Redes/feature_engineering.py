import pandas as pd
import numpy as np

def calculate_rtt_stats(df):
    # Expande lista de RTTs em colunas para cálculo vetorizado
    print("Calculando estatísticas de RTT...")
    
    rtt_expanded = pd.DataFrame(df['rtts_parsed'].tolist(), index=df.index)
    
    df['rtt_mean'] = rtt_expanded.mean(axis=1).astype('float32')
    df['rtt_std'] = rtt_expanded.std(axis=1).astype('float32')
    df['rtt_min'] = rtt_expanded.min(axis=1).astype('float32')
    df['rtt_max'] = rtt_expanded.max(axis=1).astype('float32')
    
    # Calcula taxa de perda de pacotes
    df['packet_loss_ratio'] = 1 - (df['total_replies_last_hop'] / df['total_probes_sent'].replace(0, 1))
    
    return df

def add_temporal_features(df):
    # Cria features baseadas em séries temporais (lags, diffs, rolling windows)
    print("Gerando features temporais...")
    
    df = df.sort_values(by=['tr_src', 'tr_dst', 'seconds_since_start'])
    grouped = df.groupby(['tr_src', 'tr_dst'])
    
    # Cria lags e diferenças para capturar variações ao longo do tempo
    cols_to_lag = ['rtt_mean', 'rtt_std', 'packet_loss_ratio']
    for col in cols_to_lag:
        df[f'prev_{col}'] = grouped[col].shift(1)
        df[f'diff_{col}'] = df[col] - df[f'prev_{col}']
    
    df['prev_seconds'] = grouped['seconds_since_start'].shift(1)
    df['time_since_last'] = df['seconds_since_start'] - df['prev_seconds']
    
    df['volatility_rtt_mean'] = grouped['rtt_mean'].transform(lambda x: x.rolling(window=5, min_periods=2).std())
    df['rolling5_mean_rtt'] = grouped['rtt_mean'].transform(lambda x: x.rolling(window=5, min_periods=2).mean())
    df['rolling5_std_rtt'] = grouped['rtt_std'].transform(lambda x: x.rolling(window=5, min_periods=2).mean())
    
    safe_volatility = df['volatility_rtt_mean'].replace(0, 1)
    df['z_score_rtt'] = (df['rtt_mean'] - df['rolling5_mean_rtt']) / safe_volatility
    
    df['packet_loss_trend'] = grouped['packet_loss_ratio'].transform(lambda x: x.rolling(window=5, min_periods=2).mean())
    
    return df
