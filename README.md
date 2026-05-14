# Integrated Credit Risk Modeling, Validation & Monitoring Framework

## Project Overview

This project demonstrates an end-to-end integrated credit risk analytics framework covering:

- Probability of Default (PD)
- Loss Given Default (LGD)
- Exposure at Default (EAD)
- Expected Loss (EL)
- Model Validation
- Model Monitoring
- Governance-Oriented Reporting

The framework was developed using Lending Club loan data and designed to demonstrate practical credit risk modeling and model risk management concepts including validation, monitoring, calibration, drift assessment, and governance documentation.

---

# Business Objective

Financial institutions use credit risk models to estimate borrower risk, expected losses, and portfolio stability.

This project was developed to demonstrate:

- Credit risk model development
- Validation and monitoring workflows
- Population stability assessment
- Calibration and drift analysis
- Governance-oriented model lifecycle management

The framework integrates PD, LGD, EAD, and EL concepts into a modular and reusable analytical pipeline.

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
Feature Engineering & WoE
↓
PD Modeling
↓
LGD Modeling
↓
EAD Modeling
↓
Expected Loss Calculation
↓
Validation Framework
↓
Monitoring Framework
↓
Governance Reporting
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
- matplotlib
- pickle
- Jupyter Notebook

---

# Key Results
### PD Model
- OOT AUC ≈ 0.72
- OOT Gini ≈ 0.44
- Stable score PSI

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

# Future Enhancements

Potential future enhancements include:

- IFRS9 Expected Credit Loss framework
- Challenger model implementation (XGBoost)
- Automated monitoring workflows
- ML model validation framework
- MLOps integration


# Conclusion

This project demonstrates an integrated credit risk analytics and validation framework covering PD, LGD, EAD, EL, validation, monitoring, and governance-oriented reporting.

The framework emphasizes practical implementation of model risk management concepts including validation, monitoring, calibration, drift assessment, and lifecycle governance.
