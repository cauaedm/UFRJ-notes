import pandas as pd
import numpy as np
import json

def load_data(filepath, sample_size=None, random_state=42):
    # Define tipos de dados para economizar memória
    print(f"Carregando dados de {filepath}...")
    
    dtype_dict = {
        'tr_id': 'int32',
        'tr_src': 'int32',
        'tr_dst': 'int32',
        'tr_attempts': 'int8',
        'total_probes_sent': 'int8',
        'total_replies_last_hop': 'int8',
        'route_changed': 'int8',
        'date_index': 'int16',
        'seconds_since_start': 'int32'
    }
    
    # Carrega amostra ou dataset completo dependendo do modo
    if sample_size:
        df = pd.read_csv(filepath, nrows=sample_size, dtype=dtype_dict)
        print(f"Carregadas {sample_size} linhas (modo dev)")
    else:
        df = pd.read_csv(filepath, dtype=dtype_dict)
        print(f"Dataset completo: {len(df)} linhas")

    return df

def parse_rtts_column(df):
    # Converte string JSON em lista de floats
    print("Fazendo parse de 'all_rtts'...")
    df['rtts_parsed'] = df['all_rtts'].apply(lambda x: json.loads(x) if isinstance(x, str) else [])
    return df
