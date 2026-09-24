# Slow & Low IoT DDoS Detection

## Behavioral Threat Detection & SOC Analysis

Academic cybersecurity project studying Slow & Low DDoS behavior in IoT traffic through controlled traffic generation, temporal feature engineering, machine-learning classification, baseline comparison, and SOC-oriented reporting.

> Use only in isolated and authorized environments.

## Workflow

~~~text
Controlled Traffic Generation
          ↓
Feature Engineering
          ↓
ML Training → Baseline Comparison
          ↓
SOC Analysis → Reporting / Visualization
~~~

## Detection features

- Inter-arrival time (IAT)
- Rolling traffic rates
- Flow efficiency
- Temporal behavior
- Statistical traffic characteristics

## Models

- Random Forest
- Logistic Regression
- Rule-based baseline

The original academic evaluation reported very high Random Forest results. Those figures are dataset- and methodology-specific and should not be interpreted as general real-world accuracy.

See docs/MODEL_EVALUATION.md for reproducibility and leakage-control guidance.

## Repository areas

- 1_Academic_Submission/ — academic deliverables
- docs/ — architecture and evaluation documentation
- generate_pdf.py — report generation
- locustfile.py — controlled load/traffic generation

## Safe execution

Run traffic-generation components only against systems you own or are explicitly authorized to test. Keep experiments isolated and document target scope.

## Author

Hassan Faris — Cybersecurity Engineer | SOC | Network Security

- GitHub: https://github.com/faris7assan
- LinkedIn: https://www.linkedin.com/in/hassan-faris
