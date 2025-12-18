import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
import gc
import numpy as np

from data_loader import load_data, parse_rtts_column
from feature_engineering import calculate_rtt_stats, add_temporal_features

def prepare_chunk(df_raw, is_train=True):
    """
    Process a chunk of data.
    """
    # 1. Parse
    df = parse_rtts_column(df_raw)
    
    # 2. Stats
    df = calculate_rtt_stats(df)
    
    # Drop raw to save RAM
    df.drop(columns=['all_rtts', 'rtts_parsed'], inplace=True, errors='ignore')
    
    # 3. Temporal Features
    # Note: On a chunk, this only sees local history. 
    # For training (single large chunk), it's fine.
    # For testing (batched), we accept minor boundary loss.
    df = add_temporal_features(df)
    
    # Cast residuals to float32
    float_cols = df.select_dtypes(include=['float64']).columns
    df[float_cols] = df[float_cols].astype('float32')
    
    return df

def main():
    print("=== Training Phase (Low Memory) ===")
    # Train on 500k rows (Robust, fits in RAM)
    TRAIN_SIZE = 500000 
    print(f"Loading first {TRAIN_SIZE} rows...")
    
    df_train_raw = load_data('train.csv', sample_size=TRAIN_SIZE)
    df_train = prepare_chunk(df_train_raw, is_train=True)
    
    features = [
        'rtt_mean', 'rtt_std', 'rtt_min', 'rtt_max', 'packet_loss_ratio',
        'prev_rtt_mean', 'prev_rtt_std', 'diff_rtt_mean', 'diff_rtt_std',
        'time_since_last', 'tr_attempts', 'total_probes_sent',
        'volatility_rtt_mean', 'z_score_rtt', 'packet_loss_trend'
    ]
    target = 'route_changed'
    
    # Drop NaNs for training
    df_train = df_train.dropna(subset=features + [target])
    
    X = df_train[features]
    y = df_train[target]
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
    
    print(f"Training LightGBM on {len(X_train)} samples...")
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
    
    print("\nValidation Report:")
    val_pred = clf.predict(X_val)
    print(classification_report(y_val, val_pred))
    
    # Free Train Memory
    del df_train_raw, df_train, X, y, X_train, X_val, y_train, y_val
    gc.collect()
    
    print("\n=== Inference Phase (Chunked) ===")
    
    output_file = 'my_submission.csv'
    # Write header
    with open(output_file, 'w') as f:
        f.write('tr_id,route_changed\n')
    
    CHUNK_SIZE = 200000 # 200k rows per batch (safe)
    
    # Use pandas chunksize
    chunks = pd.read_csv('test.csv', chunksize=CHUNK_SIZE)
    
    for i, chunk_raw in enumerate(chunks):
        if i % 2 == 0:
            print(f"Processing Test Chunk {i}...")
            
        # Process feature engineering on chunk
        chunk_proc = prepare_chunk(chunk_raw, is_train=False)
        
        # Predict
        preds = clf.predict(chunk_proc[features])
        
        # Save
        res = pd.DataFrame({'tr_id': chunk_proc['tr_id'], 'route_changed': preds})
        res.to_csv(output_file, mode='a', header=False, index=False)
        
        # Cleanup
        del chunk_raw, chunk_proc, preds, res
        gc.collect()
        
    print(f"Submission saved to {output_file}")

if __name__ == "__main__":
    main()
