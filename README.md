# AI-Powered Slow & Low IoT DDoS Evasion Detection 🛡️🤖

![Project Banner](https://img.shields.io/badge/Status-Active-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![AI/ML](https://img.shields.io/badge/AI-Scikit--Learn-orange)
![Cybersecurity](https://img.shields.io/badge/Domain-Cybersecurity-red)

## 📋 Project Overview

This project implements an end-to-end AI-driven cybersecurity pipeline designed to detect **"Slow & Low" DDoS attacks** in IoT environments. Unlike traditional "volumetric" DDoS attacks that overwhelm systems with massive traffic, Slow & Low attacks stay under the radar by mimicking normal traffic rates, rendering traditional threshold-based IDS ineffective.

The project is structured around three academic deliverables representing the core pillars of a modern Security Operations Center (SOC):
1. **Red Team**: Professional Threat Emulation & Attack Injection.
2. **Blue Team**: Detection Engine & AI Model Training.
3. **SOC Analyst**: Visualization, Reporting, and XAI Analysis.

---

## 🚀 Key Features

- **Stealthy Attack Emulation**: Multi-phase Slow & Low attack injection (Probe, Sustain, Cool) with jittered inter-arrival times and subnet diversity.
- **Advanced Feature Engineering**: Extraction of temporal and statistical features (IAT, Rolling Mean Rates, Flow Efficiency) to expose stealthy deviations.
- **AI-Driven Detection**: High-accuracy Random Forest and Logistic Regression models that outperform static rule-based systems.
- **Interactive Dashboard**: Real-time load-testing visualization using Streamlit and Locust.
- **Automated Reporting**: Generation of SOC-ready PDF/Image/Text reports with explainable AI (XAI) insights.

---

## 📂 Project Structure

```text
AI_Project/
├── 1_Academic_Submission/
│   ├── Red Team Deliverables/      # Threat Emulation
│   │   ├── RedTeam_20223617.py     # Attack Injection Script
│   │   ├── Load_Testing_Dashboard/ # Streamlit Visualization
│   │   └── Attack_Dataset.csv      # Base IoT Dataset
│   ├── Blue Team Deliverables/     # Detection & Defense
│   │   ├── BlueTeam_20222652.py    # ML Training & Evaluation
│   │   └── RuleBased_20222652.py   # Baseline Comparison
│   └── SOC Analyst Deliverables/   # Investigation & Reporting
│       ├── SOC_Analyst_20234029.py # Report Generation
│       └── SOC_Final_Report.txt    # Executive Summary
└── locustfile.py                   # Load Testing Configuration
```

---

## 🛠️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd AI_Project
   ```

2. **Install Dependencies**:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn streamlit locust
   ```

3. **Environment**:
   Ensure you have Python 3.8+ installed. All scripts are designed to run locally with minimal configuration.

---

## 🚦 Execution Workflow

To reproduce the project results, follow these steps in order:

### Step 1: Threat Emulation (Red Team)
Generate the stealthy attack dataset.
```bash
python "1_Academic_Submission/Red Team Deliverables/RedTeam_20223617.py"
```

### Step 2: Detection Training (Blue Team)
Train the AI models and evaluate performance against the injected dataset.
```bash
python "1_Academic_Submission/Blue Team Deliverables/BlueTeam_20222652.py"
```

### Step 3: SOC Reporting (SOC Analyst)
Generate visualizations and the final investigation report.
```bash
python "1_Academic_Submission/SOC Analyst Deliverables/SOC_Analyst_20234029.py"
```

### Step 4: Dashboard Visualization
Launch the interactive load-testing dashboard.
```bash
streamlit run "1_Academic_Submission/Red Team Deliverables/Load_Testing_Dashboard/app.py"
```

---

## 📊 Results Summary

| Model | Accuracy | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- | :--- |
| **Random Forest** | >99% | >99% | >99% | >99% |
| **Logistic Regression** | ~95% | ~92% | ~90% | ~91% |
| **Rule-Based IDS** | <5% | N/A | <1% | N/A |

*The AI models successfully identify stealthy heartbeats that bypass traditional rate-limiting rules.*

---

## 👥 Contributors

- **Red Team**: Student ID 20223617
- **Blue Team**: Student ID 20222652
- **SOC Analyst**: Student ID 20234029

---

## 📄 License
This project is for academic purposes under the AI for Cybersecurity course.
