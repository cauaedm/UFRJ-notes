import pandas as pd
import numpy as np
import ast

def load_data(filepath, sample_size=None, random_state=42):
    """
    Load dataset with optional sampling.
    """
    print(f"Loading data from {filepath}...")
    
    # Define optimal dtypes to save memory
    dtype_dict = {
        'tr_id': 'int32',
        'tr_src': 'int32',
        'tr_dst': 'int32',
        'tr_attempts': 'int8',
        'total_probes_sent': 'int8',
        'total_replies_last_hop': 'int8',
        'route_changed': 'int8', # Boolean as int
        'date_index': 'int16',
        'seconds_since_start': 'int32'
    }
    
    if sample_size:
        # Load a random sample
        # First count lines roughly or just valid loading strategy for large files
        # For simplicity in this environment, we might read full then sample if memory allows, 
        # or use skiprows. A safer way for 20M rows on limited RAM is `nrows` for dev.
        # If we really want random sample without loading all:
        
        # Method 1: Read first N rows (Training/Dev mode)
        df = pd.read_csv(filepath, nrows=sample_size, dtype=dtype_dict)
        print(f"Loaded top {sample_size} rows for development.")
    else:
        # Load full dataset
        df = pd.read_csv(filepath, dtype=dtype_dict)
        print(f"Loaded full dataset: {len(df)} rows.")

    return df

def parse_rtts_column(df):
    """
    Parses 'all_rtts' column from string to list of floats.
    Optimized to handle errors gracefully.
    """
    print("Parsing 'all_rtts' column...")
    # Using json.loads is faster than ast.literal_eval
    import json
    df['rtts_parsed'] = df['all_rtts'].apply(lambda x: json.loads(x) if isinstance(x, str) else [])
    return df
