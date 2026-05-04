"""
=============================================================================
 RULE-BASED DETECTION 20222652
 Course   : AI in Cybersecurity
 Project  : Slow & Low IoT DDoS Evasion Detection
=============================================================================
"""

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import os

def rule_based_detection(df, threshold=5.0):
    """
    Simulates a traditional IDS rule: IF packet_rate > threshold THEN Attack.
    This typically fails for 'Slow & Low' attacks because their rate is 
    purposely kept below normal traffic thresholds.
    """
    print(f"[*] Applying Rule-Based Detection (Threshold: {threshold} pkts/s)...")
    
    # Calculate packet_rate if not present
    if 'packet_rate' not in df.columns:
        df['packet_rate'] = df['pkts'] / (df['dur'] + 1e-6)
        
    # Apply rule
    df['rule_pred'] = (df['packet_rate'] > threshold).astype(int)
    
    y_true = df['label']
    y_pred = df['rule_pred']
    
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1': f1_score(y_true, y_pred, zero_division=0),
        'cm': confusion_matrix(y_true, y_pred)
    }
    
    return metrics

if __name__ == "__main__":
    # Robust path handling relative to script location
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(SCRIPT_DIR, "..", "Red Team Deliverables", "Slow_Low_Attack_Dataset.csv")
    
    if not os.path.exists(DATA_PATH):
        print(f"[!] Error: Dataset {DATA_PATH} not found.")
    else:
        df = pd.read_csv(DATA_PATH)
        
        # We test a few thresholds
        thresholds = [0.1, 1.0, 5.0, 10.0]
        
        print("\n" + "="*40)
        print(" RULE-BASED DETECTION RESULTS")
        print("="*40)
        
        for t in thresholds:
            m = rule_based_detection(df, threshold=t)
            print(f"\n>>> Threshold: {t} pkts/s")
            print(f"    Recall (Detection Rate): {m['recall']:.4f}")
            print(f"    Precision              : {m['precision']:.4f}")
            print(f"    F1-Score               : {m['f1']:.4f}")
            print(f"    Confusion Matrix:\n{m['cm']}")
            
        print("\n[CONCLUSION] Rule-based detection shows high false positives at low thresholds "
              "and zero detection at high thresholds, demonstrating its failure for Slow & Low.")
