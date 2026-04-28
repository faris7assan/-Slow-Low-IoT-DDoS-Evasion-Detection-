"""
=============================================================================
 RED TEAM - STUDENT ID: 20223617
 Project  : Slow & Low IoT DDoS Evasion Detection
 Role     : Red Team - Professional Threat Emulation (Subnet Diversity & Phasing)
=============================================================================
"""

import pandas as pd
import numpy as np
import time
import os

# ─────────────────────────────────────────────────────────────────────────────
# 0) CONFIGURATION & STUDENT PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────

STUDENT_ID = 20223617
np.random.seed(STUDENT_ID)

# MANDATORY FORMULA: (last 2 digits of STUDENT_ID / 100)
ATTACK_RATE = (STUDENT_ID % 100) / 100.0  # 17 / 100 = 0.17 pkts/sec
INTER_ARRIVAL = 1.0 / ATTACK_RATE        # ~5.88 seconds
JITTER = 0.05                             # 5% jitter for stealth

# Attacker Profile: Pro Botnet
TARGET_IP = '192.168.100.3'
SUBNETS = ['192.168.1.', '10.0.5.', '172.16.10.']
BOTNET_SIZE = 8

def generate_botnet():
    """Simulates a diverse botnet spread across multiple subnets."""
    return [f"{np.random.choice(SUBNETS)}{np.random.randint(50, 250)}" for _ in range(BOTNET_SIZE)]

BOT_IPS = generate_botnet()

# Robust path handling relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(SCRIPT_DIR, "Attack_Dataset.csv")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "Slow_Low_Attack_Dataset.csv")

# ─────────────────────────────────────────────────────────────────────────────
# 1) DATA LOADING / MOCK GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def get_base_traffic():
    """Loads BoT-IoT base traffic or generates a high-fidelity mock if missing."""
    if os.path.exists(DATASET_PATH):
        print(f"[*] Loading base traffic from {DATASET_PATH}...")
        df = pd.read_csv(DATASET_PATH)
        df['label'] = 0
        return df
    else:
        print("[!] Base dataset not found. Generating high-fidelity BoT-IoT mock...")
        n = 50000
        times = np.sort(np.random.uniform(0, 3600, n))
        df = pd.DataFrame({
            'timestamp': times,
            'saddr': [f'192.168.100.{np.random.randint(1,100)}' for _ in range(n)],
            'daddr': [TARGET_IP] * n,
            'sport': np.random.randint(1024, 65535, n),
            'dport': np.random.choice([80, 443, 1883], n),
            'proto': np.random.choice(['tcp', 'udp'], n),
            'pkts': np.random.randint(1, 10, n),
            'bytes': np.random.randint(64, 1000, n),
            'dur': np.abs(np.random.normal(1.0, 0.5, n)),
            'label': 0
        })
        return df

# ─────────────────────────────────────────────────────────────────────────────
# 2) SLOW & LOW ATTACK INJECTION (PRO VERSION)
# ─────────────────────────────────────────────────────────────────────────────

def inject_slow_low_ddos(df):
    """
    Injects a PROFESSIONAL 'Slow & Low' DDoS attack.
    Features:
    - Botnet Subnet Diversity (8 Bots, 3 Subnets)
    - Multi-Phase Attack (Probe -> Sustain -> Cool)
    - Jittered Inter-Arrival & Bursting
    - Adaptive Payload Correlation
    """
    print(f"[*] Simulating Professional Slow & Low Attack...")
    print(f"[*] Botnet Size: {BOTNET_SIZE} devices across {len(SUBNETS)} subnets.")
    
    time_col = 'timestamp' if 'timestamp' in df.columns else 'stime'
    t_start = df[time_col].min() + 500
    t_total_window = 1500
    t_end = t_start + t_total_window
    
    attack_records = []
    
    for i, bot_ip in enumerate(BOT_IPS):
        current_time = t_start + (i * 1.5) # Structured staggered start
        
        while current_time < t_end:
            # Multi-Phase Intensity Factor
            progress = (current_time - t_start) / t_total_window
            if progress < 0.2:   # Phase 1: Probe
                intensity = 0.5
            elif progress < 0.8: # Phase 2: Sustain
                intensity = 1.0
            else:               # Phase 3: Cool
                intensity = 0.3
            
            # Apply intensity to inter-arrival (Inverse)
            bot_rate_factor = np.random.uniform(0.95, 1.05) * intensity
            bot_inter_arrival = INTER_ARRIVAL / bot_rate_factor
            
            # Jitter calculation
            wait = bot_inter_arrival * (1 + np.random.uniform(-JITTER, JITTER))
            current_time += wait
            
            # 10% Bursting chance
            pkts = 2 if np.random.random() < 0.10 else 1
            
            # Adaptive Payload: smaller packets held open longer (Slowloris trait)
            pkt_bytes = np.random.randint(40, 60) if pkts == 1 else np.random.randint(100, 150)
            flow_dur = np.random.uniform(8.0, 15.0) if pkt_bytes < 50 else np.random.uniform(5.0, 10.0)
            
            record = {
                time_col: current_time,
                'saddr': bot_ip,
                'daddr': TARGET_IP,
                'sport': np.random.randint(30000, 65535),
                'dport': np.random.choice([80, 1883, 5683]),
                'proto': 'tcp',
                'pkts': pkts,
                'bytes': pkt_bytes,
                'dur': flow_dur,
                'tcp_window_size': np.random.randint(512, 1024), # Stealth: small window
                'label': 1   
            }
            attack_records.append(record)
            
    attack_df = pd.DataFrame(attack_records)
    final_df = pd.concat([df, attack_df], ignore_index=True)
    final_df = final_df.sort_values(by=time_col).reset_index(drop=True)
    
    # Advanced Feature: Flow Density Proxy
    final_df['flow_density_30s'] = final_df.groupby('daddr')['label'].transform(lambda x: x.rolling(window=20, min_periods=1).count())

    print(f"[+] Injected {len(attack_records)} professional stealthy attack records.")
    return final_df

# ─────────────────────────────────────────────────────────────────────────────
# 3) MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("="*60)
    print(f" RED TEAM PROFESSIONAL DELIVERABLE - STUDENT {STUDENT_ID}")
    print("="*60)
    
    base_df = get_base_traffic()
    dataset = inject_slow_low_ddos(base_df)
    
    dataset.to_csv(OUTPUT_PATH, index=False)
    print(f"\n[SUCCESS] Pro-level dataset generated: {OUTPUT_PATH}")
    print(f"Attack Records: {len(dataset[dataset['label'] == 1])}")
    print("="*60)
