# Slow & Low IoT DDoS Detection Architecture

```mermaid
flowchart LR
    A[Controlled Attack Emulation] --> B[Traffic Dataset]
    B --> C[Feature Engineering]
    C --> D[ML Detection]
    C --> E[Rule-Based Baseline]
    D --> F[Evaluation]
    E --> F
    F --> G[SOC Analysis]
    G --> H[Dashboard + Report]
```

## Detection Focus

The project focuses on temporal and behavioral traffic features that can help identify low-rate attacks that may evade simple volume thresholds.

## Security Boundary

Attack generation must run only in isolated, controlled environments against systems where testing is authorized.
