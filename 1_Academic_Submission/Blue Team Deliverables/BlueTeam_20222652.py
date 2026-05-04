"""
=============================================================================
 BLUE TEAM - DETECTION ENGINE 20222652
 Course   : AI in Cybersecurity
 Project  : Slow & Low IoT DDoS Evasion Detection
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import os

# ─────────────────────────────────────────────────────────────────────────────
# 1) FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────────────────────

def engineer_features(df):
    """Creates time-based and statistical features to detect Slow & Low attacks."""
    print("[*] Performing Feature Engineering...")
    
    # Handle timestamp column (support both names)
    time_col = 'timestamp' if 'timestamp' in df.columns else 'stime'
    
    # 1. Inter-arrival time (IAT)
    df['inter_arrival_time'] = df.groupby(['saddr', 'daddr'])[time_col].diff().fillna(0)
    
    # 2. Packet Rate (packets per second)
    df['packet_rate'] = df['pkts'] / (df['dur'] + 1e-6)
    
    # 3. Flow Duration (already exists but ensures consistency)
    df['flow_duration'] = df['dur']
    
    # 4. Bytes per Packet
    df['bytes_per_packet'] = df['bytes'] / (df['pkts'] + 1e-6)
    
    # 5. Packet Variance (using rolling std of bytes as a proxy if raw packet sizes aren't available)
    df['packet_variance'] = df.groupby(['saddr', 'daddr'])['bytes'].transform(lambda x: x.rolling(window=5, min_periods=1).std()).fillna(0)
    
    # 6. Flow Efficiency (packets per duration)
    df['flow_efficiency'] = df['pkts'] / (df['dur'] + 1e-6)
    
    # 7. Rate Ratio (if srate and drate exist, else mock)
    if 'srate' in df.columns and 'drate' in df.columns:
        df['rate_ratio'] = df['srate'] / (df['drate'] + 1e-6)
    else:
        df['rate_ratio'] = 1.0 # Default
        
    # 8. Rolling Mean over time window (Critical for Slow & Low)
    # We use a 10-packet window to see the trend
    df['rolling_rate_mean'] = df.groupby(['saddr', 'daddr'])['packet_rate'].transform(lambda x: x.rolling(window=10, min_periods=1).mean())
    
    # Remove metadata and original labels to prevent leakage
    features = [
        'inter_arrival_time', 'packet_rate', 'flow_duration', 
        'bytes_per_packet', 'packet_variance', 'flow_efficiency', 
        'rate_ratio', 'rolling_rate_mean', 'tcp_window_size', 'flow_density_30s'
    ]
    
    # Fill any remaining NaNs (e.g. from divisions by zero or rolling windows)
    X = df[features].fillna(0)
    y = df['label']
    
    return X, y, features

# ─────────────────────────────────────────────────────────────────────────────
# 2) MODEL TRAINING & EVALUATION
# ─────────────────────────────────────────────────────────────────────────────

def train_and_evaluate(X, y):
    """Trains and compares RF and Logistic Regression models."""
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20222652, stratify=y)
    
    # Scaling (Mandatory for Logistic Regression)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    results = {}
    
    # --- 1. Random Forest ---
    print("[*] Training Random Forest Classifier...")
    rf = RandomForestClassifier(n_estimators=100, random_state=20222652)
    rf.fit(X_train, y_train) # RF doesn't strictly need scaling
    y_pred_rf = rf.predict(X_test)
    
    results['Random Forest'] = {
        'accuracy': accuracy_score(y_test, y_pred_rf),
        'precision': precision_score(y_test, y_pred_rf),
        'recall': recall_score(y_test, y_pred_rf),
        'f1': f1_score(y_test, y_pred_rf),
        'cm': confusion_matrix(y_test, y_pred_rf),
        'model': rf
    }
    
    # --- 2. Logistic Regression (Comparison) ---
    print("[*] Training Logistic Regression Classifier...")
    lr = LogisticRegression(max_iter=1000, random_state=20222652)
    lr.fit(X_train_scaled, y_train)
    y_pred_lr = lr.predict(X_test_scaled)
    
    results['Logistic Regression'] = {
        'accuracy': accuracy_score(y_test, y_pred_lr),
        'precision': precision_score(y_test, y_pred_lr),
        'recall': recall_score(y_test, y_pred_lr),
        'f1': f1_score(y_test, y_pred_lr),
        'cm': confusion_matrix(y_test, y_pred_lr),
        'model': lr
    }
    
    return results, X_test, y_test

# ─────────────────────────────────────────────────────────────────────────────
# 3) MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Robust path handling relative to script location
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(SCRIPT_DIR, "..", "Red Team Deliverables", "Slow_Low_Attack_Dataset.csv")
    
    if not os.path.exists(DATA_PATH):
        print(f"[!] Error: Dataset {DATA_PATH} not found. Run Red Team script first.")
    else:
        df = pd.read_csv(DATA_PATH)
        X, y, feature_names = engineer_features(df)
        results, X_test, y_test = train_and_evaluate(X, y)
        
        # Display Results
        print("\n" + "="*40)
        print(" BLUE TEAM DETECTION RESULTS")
        print("="*40)
        for model_name, metrics in results.items():
            print(f"\n>>> {model_name}:")
            print(f"    Accuracy  : {metrics['accuracy']:.4f}")
            print(f"    Precision : {metrics['precision']:.4f}")
            print(f"    Recall    : {metrics['recall']:.4f}")
            print(f"    F1-Score  : {metrics['f1']:.4f}")
            print("    Confusion Matrix:")
            print(metrics['cm'])
            fp = metrics['cm'][0][1]
            fn = metrics['cm'][1][0]
            print(f"    False Positives (FP): {fp}")
            print(f"    False Negatives (FN): {fn}")
        
        # Feature Importance for RF
        importances = results['Random Forest']['model'].feature_importances_
        feat_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)
        print("\n[*] Feature Importance (Random Forest):")
        print(feat_df)
        
        print("\n[SUCCESS] Blue Team Analysis Complete.")
