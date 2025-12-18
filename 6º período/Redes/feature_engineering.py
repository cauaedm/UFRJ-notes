import pandas as pd
import numpy as np

def calculate_rtt_stats(df):
    """
    Calculates basic statistics from the parsed RTT list.
    OPTIMIZED: Uses list expansion instead of apply.
    """
    print("Calculating RTT statistics (Vectorized)...")
    
    # Expand list column to dataframe columns
    rtt_expanded = pd.DataFrame(df['rtts_parsed'].tolist(), index=df.index)
    
    # Calculate stats across columns (axis=1)
    # Cast to float32 to save memory
    df['rtt_mean'] = rtt_expanded.mean(axis=1).astype('float32')
    df['rtt_std'] = rtt_expanded.std(axis=1).astype('float32') # Jitter
    df['rtt_min'] = rtt_expanded.min(axis=1).astype('float32')
    df['rtt_max'] = rtt_expanded.max(axis=1).astype('float32')
    
    # Calculate packet loss ratio
    df['packet_loss_ratio'] = 1 - (df['total_replies_last_hop'] / df['total_probes_sent'].replace(0, 1))
    
    return df

def add_temporal_features(df):
    """
    Adds robust temporal features including Volatility and Burstiness.
    Requires dataframe to be sorted by [src, dst, time].
    """
    print("Generating temporal features (Lags, Rolling, Volatility)...")
    
    # Ensure sorted
    df = df.sort_values(by=['tr_src', 'tr_dst', 'seconds_since_start'])
    
    # Group by src-dst
    grouped = df.groupby(['tr_src', 'tr_dst'])
    
    # 1. Simple Lags & Diffs (Differential Latency/Jitter)
    cols_to_lag = ['rtt_mean', 'rtt_std', 'packet_loss_ratio']
    for col in cols_to_lag:
        df[f'prev_{col}'] = grouped[col].shift(1)
        df[f'diff_{col}'] = df[col] - df[f'prev_{col}'] # Differential Latency/Jitter
    
    # 2. Time gap
    df['prev_seconds'] = grouped['seconds_since_start'].shift(1)
    df['time_since_last'] = df['seconds_since_start'] - df['prev_seconds']
    
    # 3. Burstiness & Volatility (Rolling Window = 5)
    # Volatility = Standard Deviation of the Mean RTTs over time
    df['volatility_rtt_mean'] = grouped['rtt_mean'].transform(lambda x: x.rolling(window=5, min_periods=2).std())
    
    # Rolling Mean for Baseline
    df['rolling5_mean_rtt'] = grouped['rtt_mean'].transform(lambda x: x.rolling(window=5, min_periods=2).mean())
    df['rolling5_std_rtt'] = grouped['rtt_std'].transform(lambda x: x.rolling(window=5, min_periods=2).mean()) # Avg Jitter
    
    # Spike Detection (Z-Score approximation)
    # (Current - RollingMean) / Volatility
    # Avoid division by zero
    safe_volatility = df['volatility_rtt_mean'].replace(0, 1) # If volatility is 0, replace with 1 to avoid Inf
    df['z_score_rtt'] = (df['rtt_mean'] - df['rolling5_mean_rtt']) / safe_volatility
    
    # Packet Loss Trend
    df['packet_loss_trend'] = grouped['packet_loss_ratio'].transform(lambda x: x.rolling(window=5, min_periods=2).mean())
    
    return df
