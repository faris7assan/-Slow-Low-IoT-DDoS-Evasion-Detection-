# Model Evaluation Notes

The reported >99% Random Forest results are academic results tied to the project's dataset and evaluation procedure. They should not be presented as general real-world detection accuracy.

## Reproducibility requirements

A stronger evaluation should document:

- Dataset source and class distribution
- Exact train/test split
- Random seed
- Feature list and preprocessing
- Whether samples from the same flow/device can cross the split
- Hyperparameters
- Confusion matrix
- Precision, recall, F1, and false-positive rate
- Baseline detector configuration
- Performance on an unseen device or time window

## Leakage check

For traffic detection, random row-level splitting can overestimate generalization when correlated samples from the same flow or device appear in both training and test sets. Prefer grouped or time-based splits where appropriate.

## Recommended reporting

Report per-class metrics and a confusion matrix in addition to accuracy. For SOC use cases, explicitly discuss false positives and false negatives because operational cost is asymmetric.
