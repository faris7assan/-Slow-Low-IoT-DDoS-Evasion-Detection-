# Slow & Low IoT DDoS Detection

### AI-Assisted Threat Detection and SOC Analysis

This project implements an end-to-end cybersecurity pipeline for detecting **Slow & Low DDoS attacks in IoT traffic**. The project combines controlled threat emulation, feature engineering, machine-learning-based detection, and SOC-oriented reporting.

> Developed for academic and authorized security-testing environments only.

## Security Workflow

```text
Threat Emulation
      ↓
Traffic / Dataset Generation
      ↓
Feature Engineering
      ↓
ML Detection
      ↓
Baseline Comparison
      ↓
SOC Analysis & Reporting
```

## Project Roles

### Red Team
- Controlled Slow & Low attack emulation
- Multi-phase traffic generation
- Probe / Sustain / Cool phases
- Jittered inter-arrival times
- Traffic dataset generation

### Blue Team
- Traffic feature extraction
- Machine-learning model training
- Random Forest classification
- Logistic Regression comparison
- Rule-based baseline evaluation

### SOC Analyst
- Detection result analysis
- Visualization
- Explainable analysis
- Automated security reporting

## Detection Features

The project extracts temporal and statistical traffic characteristics such as:

- Inter-arrival time (IAT)
- Rolling traffic rates
- Flow efficiency
- Traffic behavior over time

These features are used to identify low-rate traffic patterns that can be difficult to detect using simple volume-based thresholds.

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Streamlit
- Locust

## Project Structure

```text
AI_Project/
├── 1_Academic_Submission/
│   ├── Red Team Deliverables/
│   │   ├── RedTeam_20223617.py
│   │   ├── Load_Testing_Dashboard/
│   │   └── Attack_Dataset.csv
│   ├── Blue Team Deliverables/
│   │   ├── BlueTeam_20222652.py
│   │   └── RuleBased_20222652.py
│   └── SOC Analyst Deliverables/
│       ├── SOC_Analyst_20234029.py
│       └── SOC_Final_Report.txt
└── locustfile.py
```

## Installation

```bash
git clone https://github.com/faris7assan/-Slow-Low-IoT-DDoS-Evasion-Detection-.git
cd -Slow-Low-IoT-DDoS-Evasion-Detection-
pip install pandas numpy scikit-learn matplotlib seaborn streamlit locust
```

## Execution

### 1. Threat Emulation

```bash
python "1_Academic_Submission/Red Team Deliverables/RedTeam_20223617.py"
```

### 2. Detection Training

```bash
python "1_Academic_Submission/Blue Team Deliverables/BlueTeam_20222652.py"
```

### 3. SOC Reporting

```bash
python "1_Academic_Submission/SOC Analyst Deliverables/SOC_Analyst_20234029.py"
```

### 4. Dashboard

```bash
streamlit run "1_Academic_Submission/Red Team Deliverables/Load_Testing_Dashboard/app.py"
```

## Evaluation

The original academic evaluation reported the following model performance:

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---:|---:|---:|---:|
| Random Forest | >99% | >99% | >99% | >99% |
| Logistic Regression | ~95% | ~92% | ~90% | ~91% |
| Rule-Based IDS | <5% | N/A | <1% | N/A |

These figures are retained as the project's academic results and should be interpreted in the context of the dataset and evaluation methodology used in the project.

## Why It Matters

Slow & Low attacks deliberately keep traffic volume relatively low, making simple threshold-based detection less effective. This project explores how behavioral and temporal features can improve detection of stealthier network attacks.

## Author

**Hassan Faris**  
Cybersecurity Graduate | SOC | Threat Detection | Network Security

GitHub: https://github.com/faris7assan
