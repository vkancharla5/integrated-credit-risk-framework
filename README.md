# Integrated Credit Risk Modeling, Validation & MRM Framework
### Basel III-aligned PD/LGD/EAD modeling | IFRS 9 ECL-compatible | SR 11-7 MRM governance

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Basel III](https://img.shields.io/badge/Regulatory-Basel%20III%20IRB-green)
![IFRS9](https://img.shields.io/badge/IFRS%209-ECL%20Compatible-green)
![SR11-7](https://img.shields.io/badge/MRM-SR%2011--7%20Aligned-orange)

> **Regulatory context:** This framework replicates the model lifecycle a bank follows under 
> Basel III IRB approach — developing PD, LGD, EAD models, calculating Expected Loss (EL = PD × 
> LGD × EAD), validating against champion/challenger benchmarks, and producing SR 11-7 aligned 
> governance documentation. forming the foundational EL framework used in IFRS 9 / Ind AS 109 Expected Credit Loss (ECL) estimation
> Expected Credit Loss (ECL) staging logic.

**Framework covers:** PD · LGD · EAD · Expected Loss · Champion–Challenger Validation · 
PSI Monitoring · Calibration · Model Risk Governance (MDD, MID, Risk Register, Monitoring Plan)

---

## Regulatory Alignment

| Framework | Coverage in this project |
|-----------|--------------------------|
| **Basel III IRB** | PD, LGD, EAD model development; RWA-oriented credit risk estimation |
| **IFRS 9 / Ind AS 109** | EL = PD × LGD × EAD maps directly to 12-month and lifetime ECL; Stage 1/2/3 classification logic |
| **SR 11-7 (Fed MRM guidance)** | Independent validation, challenger benchmarking, governance documentation, monitoring thresholds |
| **RBI Model Risk Guidelines** | Model lifecycle management, drift escalation, recalibration assessment |
---
## IFRS 9 / Ind AS 109 Connection

Under IFRS 9, banks classify loans into three stages based on credit deterioration:

- **Stage 1** — No significant increase in credit risk → 12-month ECL = PD(12m) × LGD × EAD
- **Stage 2** — Significant increase in credit risk → Lifetime ECL
- **Stage 3** — Credit-impaired (defaulted) → Lifetime ECL, interest on net carrying amount

The EL framework in this project (EL = PD × LGD × EAD) directly implements the Stage 1 
12-month ECL calculation. The PD model's calibration pipeline supports lifetime PD estimation 
for Stage 2/3 classification. Indian banks operating under RBI's Ind AS 109 mandate use 
similar model architecture principles.
---

# Dataset

This project uses publicly available Lending Club loan data for credit risk modeling and validation workflows.

Dataset source:
https://www.kaggle.com/datasets/wordsforthewise/lending-club

The project uses:
- loan_data_2007_2014.csv (development/training dataset)
- loan_data_2015.csv (monitoring/validation dataset)

Due to GitHub file size limitations, datasets are hosted externally.

Dataset download links:
- loan_data_2007_2014.csv : https://drive.google.com/file/d/1XV19UXxh-wBsU6QlIzo1dATyDm8ibtIk/view?usp=drive_link
- loan_data_2015.csv : https://drive.google.com/file/d/1GuZ489x68HQwduqUztke4Wbd3XTxyAQu/view?usp=drive_link

After downloading, place files inside:

```bash
data/
├── loan_data_2007_2014.csv
└── loan_data_2015.csv
```

## To Run the Pipelines

1. Download the datasets
2. Place CSV files inside the `data/` folder
3. Run notebooks from the `pipeline/` folder

# Key Components

## 1. Data Preprocessing
- Missing value handling
- Date conversion
- Outlier treatment
- Data quality checks
- Target variable creation

## 2. Feature Engineering & WoE Transformation
- Binning strategy implementation
- Weight of Evidence (WoE) transformation
- Information Value (IV) based feature selection

## 3. PD Modeling
- Logistic Regression
- Scorecard-oriented framework
- ROC / AUC evaluation
- KS and Gini analysis
- Calibration pipeline

## 4. LGD Modeling
- Two-stage recovery modeling approach
- Recovery rate estimation
- Segment-level validation

## 5. EAD Modeling
- Exposure estimation framework
- Utilization behavior analysis
- Stability assessment

## 6. Expected Loss Framework

EL = PD × LGD × EAD

## 7. Validation Framework
- AUC
- KS Statistic
- Gini Coefficient
- Backtesting
- Calibration assessment
- Brier Score
- MAE / RMSE
- Distribution comparison
- Segment analysis
- Stability checks

## 8. Monitoring Framework
- Score PSI monitoring
- Feature PSI monitoring
- Drift analysis
- Threshold-based escalation review
- Calibration monitoring

---

# Integrated Framework Architecture

```text
Raw Data
   ↓
Preprocessing
   ↓
WoE / Binning
   ↓
PD / LGD / EAD
   ↓
Expected Loss
   ↓
IFRS9 Staging
   ↓
Validation
   ↓
Monitoring
   ↓
Governance Artifacts
```
---

# Folder Structure

```bash
Credit risk project/
│
├── src/
├── pipeline/
├── artifacts/
├── Reports/
├── governance_artifacts/
└── README.md
```

# Pipeline Notebooks

| Notebook                              | Purpose                     |
| ------------------------------------- | --------------------------- |
| exploratory_data_analysis.ipynb       | Initial data exploration    |
| pd_model_training_pipeline.ipynb      | PD model training pipeline  |
| calibration_pipeline.ipynb            | PD calibration workflow     |
| model_validation.ipynb                | PD validation framework     |
| model_monitoring_pipeline.ipynb       | Monitoring and PSI analysis |
| integrated_credit_risk_pipeline.ipynb | LGD, EAD and EL framework   |

# Governance Artifacts

The repository includes governance-oriented documentation artifacts including:

- Model Development Document
- Model Implementation Document
- Model Inventory
- Model Monitoring Plan
- Model Risk Register

# Technologies Used
- Python
- pandas
- numpy
- scikit-learn
- statsmodels
- xgboost, lightgbm (challenger model benchmarking)
- SHAP (model interpretability — planned)
- matplotlib
- pickle
- Jupyter Notebook

---

## Key Results

### Champion Model — Logistic Regression (Basel III IRB / IFRS 9 Compliant)

| Metric | Train | Test | OOT (2015) | Interpretation |
|--------|-------|------|------------|----------------|
| AUC | 0.6738 | 0.6711 | 0.7217 | Good discriminatory power |
| Gini | 0.3477 | 0.3423 | 0.4434 | Strong on unseen data |
| KS Statistic | 0.2517 | 0.2496 | 0.3282 | Good separation of good/bad |
| Score PSI | — | — | 0.043 < 0.10 | Stable — no drift detected |
| Brier Score | — | — | 0.018 | Calibration quality |

> **Note:** OOT performance exceeds test performance — indicates the 
> model generalises well and is not overfitted to the development sample.

---

### Champion vs Challenger — OOT Validation (2015 Holdout Dataset)

All models trained on 2007–2014 Lending Club data, evaluated on identical 
2015 OOT holdout — ensuring fair, unbiased comparison.

| Model | OOT AUC | OOT Gini | OOT KS | Regulatory Decision |
|-------|---------|----------|--------|-------------------|
| **Logistic Regression (Champion)** | **0.7217** | **0.4434** | **0.3282** | ✅ Retained — Basel III IRB compliant |
| XGBoost (Challenger 1) | 0.7113 | 0.4225 | 0.3122 | ⚠️ Rejected — see note below |
| LightGBM (Challenger 2) | 0.7181 | 0.4363 | 0.3204 | ⚠️ Rejected — see note below |
| Random Forest (Challenger 3) | 0.6206 | 0.2412 | 0.1857 | ⚠️ Rejected — see note below |

> **Validation finding:** Logistic Regression outperforms all challenger 
> models on every OOT metric (AUC, Gini, KS). Additionally, Basel III IRB 
> and IFRS 9 require model interpretability, coefficient significance testing 
> (p-values), and regulatory explainability — constraints that black-box 
> ensemble models cannot satisfy. Champion model is retained on both 
> performance and regulatory grounds.

---

### IFRS 9 / Ind AS 109 ECL Framework

| Component | Implementation | Dataset |
|-----------|---------------|---------|
| Stage 1 (Performing) | 12-month ECL = PD × LGD × EAD | Lending Club 2007–2014 |
| Stage 2 (SICR) | Lifetime ECL — SICR triggers: delinquency, grade migration, PD > 20% | Lending Club 2007–2014 |
| Stage 3 (Impaired) | Lifetime ECL — aligned with config.BAD_STATUS | Lending Club 2007–2014 |
| Lifetime PD | Empirical survival curve scaling — 2007–2014 cohort MOB | Lending Club 2007–2014 |
| Macro Scenarios | Base (50%) / Adverse (35%) / Severe (15%) — calibrated from 2007–09 stress cohort | External + LC cohort |

---

### Model Monitoring — Score & Feature Stability

| Metric | Value | Status | Action |
|--------|-------|--------|--------|
| Score PSI (PD) | < 0.10 | 🟢 Stable | No action required |
| Feature PSI — majority | < 0.10 | 🟢 Stable | No action required |
| Feature PSI — flagged | 0.10–0.25 | 🟡 Moderate | Monitor |
| Recalibration trigger | > 0.25 | 🔴 Threshold | Investigate / recalibrate |

---

### Governance Artifacts Produced

| Artifact | Purpose | Regulatory Alignment |
|----------|---------|---------------------|
| Model Development Document (MDD) | Documents methodology, assumptions, limitations | Basel III / SR 11-7 |
| Model Implementation Document (MID) | Deployment specifications and controls | SR 11-7 |
| Validation Report | Independent challenge of model performance | SR 11-7 §4 |
| Monitoring Plan | Ongoing performance tracking thresholds | Basel III / RBI MRM |
| Model Risk Register | Risk inventory and escalation framework | SR 11-7 / RBI |
| Model Inventory | Full lifecycle tracking | SR 11-7 §3 |

### LGD Validation
- Low prediction bias
- Reasonable recovery estimation alignment
- Stable segment-level behavior

### EAD Validation
- Low systematic bias
- Reasonable exposure estimation stability
- Stable distribution behavior

### Monitoring
- Low overall score drift
- Stable portfolio-level prediction behavior
- Threshold-based monitoring framework implemented

- Modular and reusable pipeline structure implemented

# Model Risk Management Alignment

The framework demonstrates practical implementation of:

- Model lifecycle management
- Validation concepts
- Monitoring and drift analysis
- Recalibration assessment
- Governance documentation
- Threshold-based escalation review
- Stability monitoring

The project was structured using modular pipelines and reusable artifacts to support reproducibility and governance-oriented workflows.

# How to Run

## Clone Repository

```bash
git clone https://github.com/vkancharla5/integrated-credit-risk-framework.git
```
## Install Dependencies

```bash
pip install pandas numpy scikit-learn statsmodels matplotlib
```

## Run Pipelines

Execute notebooks in the following order:

1. exploratory_data_analysis.ipynb
2. pd_model_training_pipeline.ipynb
3. calibration_pipeline.ipynb
4. model_validation.ipynb
5. model_monitoring_pipeline.ipynb
6. integrated_credit_risk_pipeline.ipynb

# Model Artifacts

Serialized model artifact files (`.pkl`) are not included in this repository due to GitHub file size limitations.

Artifacts can be regenerated by running the training and pipeline notebooks available in the `pipeline/` folder.

# Reports Included
- Validation Report
- Model Validation Summary Report
- Monitoring Report
- Model Monitoring Summary Report

# Limitations
- Public Lending Club data may not fully represent proprietary banking portfolios.
- LGD and EAD models use proxy variables due to dataset limitations.
- Simplified exposure assumptions were used for EAD estimation.
- Real-world environments may require additional governance integration and production controls.

## Completed vs Planned Enhancements

**Already implemented:**
- ✅ Champion–Challenger validation (LR vs XGBoost vs LightGBM vs Random Forest)
- ✅ IFRS 9 ECL-compatible EL framework (PD × LGD × EAD)
- ✅ SR 11-7 aligned governance documentation

**Planned:**
- IFRS 9 Stage 1/2/3 explicit classification notebook
- SHAP-based explainability for ML challenger models
- Automated monitoring pipeline (scheduled PSI alerts)


# Conclusion

This project demonstrates an integrated credit risk analytics and validation framework covering PD, LGD, EAD, EL, validation, monitoring, and governance-oriented reporting.

The framework emphasizes practical implementation of model risk management concepts including validation, monitoring, calibration, drift assessment, and lifecycle governance.
