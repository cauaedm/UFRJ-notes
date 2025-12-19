import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
import gc
import numpy as np

from data_loader import load_data, parse_rtts_column
from feature_engineering import calculate_rtt_stats, add_temporal_features

def prepare_chunk(df_raw, is_train=True):
    # Pipeline completo de feature engineering em um chunk de dados
    df = parse_rtts_column(df_raw)
    df = calculate_rtt_stats(df)
    df.drop(columns=['all_rtts', 'rtts_parsed'], inplace=True, errors='ignore')
    df = add_temporal_features(df)
    
    # Converte para float32 para economizar memória
    float_cols = df.select_dtypes(include=['float64']).columns
    df[float_cols] = df[float_cols].astype('float32')
    
    return df

def main():
    # Treina modelo com subset dos dados e aplica em chunks no teste
    print("=== Fase de Treinamento ===")
    TRAIN_SIZE = 500000
    print(f"Carregando primeiras {TRAIN_SIZE} linhas...")
    
    df_train_raw = load_data('train.csv', sample_size=TRAIN_SIZE)
    df_train = prepare_chunk(df_train_raw, is_train=True)
    
    features = [
        'rtt_mean', 'rtt_std', 'rtt_min', 'rtt_max', 'packet_loss_ratio',
        'prev_rtt_mean', 'prev_rtt_std', 'diff_rtt_mean', 'diff_rtt_std',
        'time_since_last', 'tr_attempts', 'total_probes_sent',
        'volatility_rtt_mean', 'z_score_rtt', 'packet_loss_trend'
    ]
    target = 'route_changed'
    
    df_train = df_train.dropna(subset=features + [target])
    
    X = df_train[features]
    y = df_train[target]
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
    
    print(f"Treinando LightGBM com {len(X_train)} amostras...")
    clf = lgb.LGBMClassifier(
        n_estimators=300,
        learning_rate=0.03,
        num_leaves=31,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced',
        verbose=-1
    )
    
    clf.fit(X_train, y_train, eval_set=[(X_val, y_val)], callbacks=[lgb.early_stopping(20)])
    
    print("\nRelatório de Validação:")
    val_pred = clf.predict(X_val)
    print(classification_report(y_val, val_pred))
    
    # Libera memória antes da inferência
    del df_train_raw, df_train, X, y, X_train, X_val, y_train, y_val
    gc.collect()
    
    print("\n=== Fase de Inferência ===")
    
    output_file = 'my_submission.csv'
    with open(output_file, 'w') as f:
        f.write('tr_id,route_changed\n')
    
    # Processa teste em chunks para não estourar memória
    CHUNK_SIZE = 200000
    chunks = pd.read_csv('test.csv', chunksize=CHUNK_SIZE)
    
    for i, chunk_raw in enumerate(chunks):
        if i % 2 == 0:
            print(f"Processando chunk {i}...")
            
        chunk_proc = prepare_chunk(chunk_raw, is_train=False)
        preds = clf.predict(chunk_proc[features])
        
        res = pd.DataFrame({'tr_id': chunk_proc['tr_id'], 'route_changed': preds})
        res.to_csv(output_file, mode='a', header=False, index=False)
        
        del chunk_raw, chunk_proc, preds, res
        gc.collect()
        
    print(f"Submissão salva em {output_file}")

if __name__ == "__main__":
    main()
