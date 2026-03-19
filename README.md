# CyberShield AI — Network Attack Classifier

Classifying network intrusion attacks using Logistic Regression on 101K+ real network traffic records with 14 behavioral and system features.

## What It Does

Takes a customer's packet size, CPU usage, RAM usage, login attempts, active sessions, protocol type and other network metrics — predicts which type of cyber attack is occurring (or if traffic is normal).

## Pipeline

1. **Cleaning** — Removed duplicates (~1500), filled missing values with median
2. **EDA** — Class balance chart, CPU/RAM distribution, KDE plots, correlation heatmap, boxplots
3. **Encoding** — LabelEncoder for 4 categorical features (Protocol, Device, Network Type, City)
4. **Imbalance** — SMOTE (sampling_strategy='not majority') to handle 70%/30% class imbalance
5. **Modeling** — Baseline model → GridSearchCV (225 combinations, 5-Fold Stratified CV)
6. **Tuning** — GridSearchCV with C, penalty, solver, l1_ratio parameters
7. **Evaluation** — Classification Report, Confusion Matrix, ROC Curve, Feature Importance, Cross-Validation

## Results

| Metric | Value |
|--------|-------|
| Test Accuracy | 99.99% |
| F1-macro (CV) | 98.88% ± 0.25% |
| Precision | 99.97% |
| Recall | 99.99% |
| Best Model | C=0.01, penalty=l2, solver=sag |

Overfitting gap: 0.00 (Train = Test = 1.0). Top features: Giriş_Cəhdi (login attempts), Aktiv_Sessiya (active sessions), RAM_İstifadəsi.

## Quick Start
```
pip install -r requirements.txt
python app.py
```

## Live Demo

[cybersecurity-attack-classifier.onrender.com](https://cybersecurity-attack-classifier.onrender.com)

---

Elton Valiyev — [LinkedIn](https://www.linkedin.com/in/eltonvaliyev/)
