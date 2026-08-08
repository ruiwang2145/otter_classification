# 🦦 Sea Otter Subspecies Classification

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-orange.svg)](https://scikit-learn.org/)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A **binary classification** project using real-world sea otter morphometric data to distinguish between two subspecies — **Enhydra lutris kenyoni** (Alaska / Northern) and **Enhydra lutris nereis** (California / Southern). The project focuses on the complete applied machine learning pipeline: from heterogeneous data alignment through feature selection to multi-model comparison and interpretability analysis.

---

> 🇨🇳 中文版请见 [README_CN.md](README_CN.md)

---

## 📋 Table of Contents

- [Data Sources](#-data-sources)
- [Project Structure](#-project-structure)
- [Dataset Overview](#-dataset-overview)
- [Methodology](#-methodology)
  - [Data Alignment & Cleaning](#1-data-alignment--cleaning)
  - [Feature Selection](#2-feature-selection)
  - [Models Compared](#3-models-compared)
  - [Hyperparameter Tuning](#4-hyperparameter-tuning)
- [Key Results](#-key-results)
- [Visualizations](#-visualizations)
- [Interpretability & Ethics](#-interpretability--ethics)
- [Installation & Usage](#-installation--usage)
- [Dependencies](#-dependencies)
- [Limitations & Future Work](#-limitations--future-work)
- [Acknowledgements](#-acknowledgements)

---

## 📊 Data Sources

Two public datasets provided by the **United States Geological Survey (USGS)** via ScienceBase:

| Subspecies | Region | Dataset | Source |
|---|---|---|---|
| *E. l. kenyoni* | Alaska (North) | `alaska_seaotter.csv` | [sciencebase.gov](https://www.sciencebase.gov/catalog/item/61a28ad0d34eb622f6974679) |
| *E. l. nereis* | California (South) | `california_seaotter.csv` | [sciencebase.gov](https://www.sciencebase.gov/catalog/item/5d4b3de5e4b01d82ce8df3f3) |

**Initial data challenges:**

- Inconsistent column naming and encoding across the two sources
- Placeholder values (e.g. `-9` used as missing in the Alaska dataset)
- Substantial missingness in morphological measurements
- Significant sample size imbalance between the two subspecies
- Juvenile individuals with unstable morphometric features

---

## 📁 Project Structure

```
otter_classification/
├── 24209702_OtterClassification.ipynb  # Main analysis notebook
├── alaska_seaotter.csv                 # Alaska (kenyoni) capture data
├── california_seaotter.csv             # California (nereis) capture data
├── README.md                           # English documentation (you are here)
├── README_CN.md                        # Chinese documentation
└── dataset/
    ├── alaska_seaotter.csv             # Dataset copy (Alaska)
    ├── california_seaotter.csv         # Dataset copy (California)
    └── datafile.md                     # Data description notes
```

---

## 🐾 Dataset Overview

After alignment, the unified feature space includes **6 morphometric variables**:

| Feature | Description | Unit |
|---|---|---|
| `weight` | Body weight | kg |
| `length` | Body length | cm |
| `tail_length` | Tail length | cm |
| `girth` | Body girth circumference | cm |
| `paw_width` | Right paw width | mm |
| `canine_width` | Canine tooth diameter | mm |

**Final modeling features** (selected based on completeness & biological relevance):

| Feature | Biological Significance |
|---|---|
| `weight` | Northern otters are generally larger and heavier |
| `paw_width` | Known to differ between subspecies |
| `canine_width` | Southern otters have narrower jaws and smaller canines |

> *Reference: Timm-Davis et al. (2015), Wilson et al. (1991) — see notebook for full citations.*

---

## 🔬 Methodology

### 1. Data Alignment & Cleaning

| Step | Detail |
|---|---|
| **Field mapping** | Mapped equivalent fields across heterogeneous column names (`true_standard_lgth` ↔ `Length (cm)`) |
| **Placeholder removal** | Replaced `-9` with `NaN` in Alaska dataset |
| **Juvenile filtering** | Removed individuals with `AgeClass ≠ Adult` or `weight < 10 kg` / `length < 100 cm` |
| **Missing value handling** | `tail_length` and `girth` excluded due to excessive missingness; remaining rows with missing values dropped |
| **Class balancing** | Down-sampled the majority class to match the minority class size for fair comparison |

### 2. Feature Selection

Based on EDA, PCA analysis, and domain literature, **3 features** were selected:

- ✅ `weight` — strong discriminative signal
- ✅ `paw_width` — subspecies-level anatomical difference
- ✅ `canine_width` — jaw morphology known to vary by subspecies
- ❌ `tail_length`, `girth` — excluded due to high missingness and low discriminative power

### 3. Models Compared

Five classification models were trained and evaluated, each offering different strengths:

| Model | Type | Rationale |
|---|---|---|
| **Logistic Regression** | Linear classifier | Simple, interpretable baseline |
| **SVM (RBF kernel)** | Kernel-based | Captures non-linear boundaries |
| **Decision Tree** | Rule-based | Visual and interpretable decision logic |
| **Random Forest** | Ensemble (bagging) | Robust to overfitting; best performer |
| **Neural Network (MLP)** | Deep learning | Tests for hidden non-linear patterns |

### 4. Hyperparameter Tuning

The best model (Random Forest) was tuned with **GridSearchCV + 5-fold cross-validation**:

| Parameter | Search Space | Best Value |
|---|---|---|
| `max_depth` | `[3, 5, 7, None]` | `None` |
| `min_samples_split` | `[2, 5, 10]` | `2` |

---

## 🏆 Key Results

### Model Performance Comparison

All metrics reported on the **held-out test set (20%)** after cleaning and class balancing:

| Model | Accuracy | F1-score | Precision | Recall |
|---|---|---|---|---|
| Logistic Regression | 0.672 | 0.664 | 0.690 | 0.672 |
| SVM | 0.656 | 0.649 | 0.659 | 0.656 |
| Decision Tree | 0.803 | 0.802 | 0.819 | 0.803 |
| **Random Forest** | **0.867** | **0.867** | **0.867** | **0.867** |
| Neural Network (MLP) | 0.623 | 0.613 | 0.655 | 0.623 |

### Final Tuned Model

| Metric | Value |
|---|---|
| **Algorithm** | Random Forest (100 estimators, tuned) |
| **Accuracy** | **0.867** |
| **F1-score** | **0.867** |
| **Precision** | **0.867** |
| **Recall** | **0.867** |
| **Cross-validation** | 5-fold GridSearchCV |

> Random Forest consistently outperformed other models, with SVM achieving a baseline accuracy of around 60% for context.

### Key Findings

- 🧬 **Measurable differences exist**: Sea otter subspecies can be distinguished using simple morphometric measurements alone.
- 📏 **Weight is the strongest feature**: Aligns with biological expectation — northern otters are larger.
- 🦷 **Canine width adds discriminative power**: Supports documented jaw morphology differences.
- 🧒 **Juvenile data degrades performance**: Removing immature individuals significantly improved generalization.
- 🌲 **Random Forest wins**: Best balance of accuracy, F1-score, and interpretability across all tested models.
- ⚠️ **~12% misclassification rate remains**: The model should be used as a decision-support tool, not a replacement for expert judgment.

---

## 📈 Visualizations

The notebook includes a comprehensive set of visualizations:

| Visualization | Purpose |
|---|---|
| Missing value heatmap | Identify data quality issues across features |
| Histograms + KDE (6 features) | Distribution analysis per morphometric variable |
| Box plots (6 features) | Outlier detection and range comparison |
| PCA scatter plot (PC1 vs PC2) | Visualize subspecies separation in 2D |
| Confusion matrix | Error analysis for best model (Random Forest) |
| Feature importance | Interpret which morphometric features drive classification |

---

## 🔍 Interpretability & Ethics

### Model Interpretability

Random Forest offers built-in feature importance measurement, making the model **more transparent than black-box alternatives** (e.g., MLP). Feature importance analysis confirmed that `weight` and `canine_width` were the two most influential predictors.

> Future work should incorporate **SHAP** or **LIME** values for instance-level explanations when deploying to biologists or conservation authorities.

### Fairness Considerations

- **Training data bias**: If one population (e.g., healthy adults) is overrepresented, the model may underperform on juveniles or malnourished specimens.
- **Conservation impact**: Incorrect subspecies classification could influence downstream research or management decisions.
- **Not a replacement for expertise**: The model should function as a **decision-support tool** alongside expert biological judgment.

---

## 🚀 Installation & Usage

### Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab (or Google Colab)

### Setup

```bash
# Clone the repository
git clone https://github.com/ruiwang2145/otter_classification.git
cd otter_classification

# Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn

# Launch the notebook
jupyter notebook 24209702_OtterClassification.ipynb
```

Run all cells in order — the notebook will:
1. Load and align the two CSV datasets
2. Perform EDA and visualize distributions
3. Clean, balance, and preprocess data
4. Train 5 classification models
5. Evaluate and compare performance
6. Tune the best model with GridSearchCV
7. Generate confusion matrix and feature importance

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `pandas` | ≥ 1.3 | Data loading, cleaning, alignment |
| `numpy` | ≥ 1.21 | Numerical operations |
| `matplotlib` | ≥ 3.5 | Static visualizations |
| `seaborn` | ≥ 0.11 | Statistical plots (heatmaps, box plots, KDE) |
| `scikit-learn` | ≥ 1.0 | Models, preprocessing, metrics, GridSearchCV |

---

## 🚧 Limitations & Future Work

### Current Limitations

- Only **3 features** used — `tail_length` and `girth` excluded due to missing data
- Dataset is **relatively small** after cleaning and balancing
- **No external validation dataset** — results are based on a single train/test split
- Class imbalance, while addressed through down-sampling, may still influence model bias

### Future Improvements

- [ ] Incorporate additional features with better imputation strategies (e.g., MICE, KNN imputation)
- [ ] Explore gradient boosting models (XGBoost, LightGBM, CatBoost)
- [ ] Apply **SHAP** for instance-level interpretability
- [ ] Validate with external or time-separated holdout data
- [ ] Add cross-validation metrics beyond GridSearch (e.g., stratified k-fold evaluation)
- [ ] Publish a more comprehensive feature engineering pipeline

---

## 🙏 Acknowledgements

This project was inspired by the **Palmer Penguins** dataset project by Dr. Allison Horst ([github.com/allisonhorst/palmerpenguins](https://github.com/allisonhorst/palmerpenguins)), which demonstrated the elegant use of body measurements to classify biological categories.

Scientific references:
- Timm-Davis, L. L., DeWitt, T. J., & Marshall, C. D. (2015). *Divergent skull morphology supports two trophic specializations in otters (Lutrinae).* PLoS ONE, 10(12), e0143236.
- Wilson, D. E., Bogan, M. A., Brownell, R. L., Burdin, A. M., & Maminov, M. K. (1991). *Geographic Variation in Sea Otters, Enhydra lutris.* Journal of Mammalogy, 72(1), 22–36.
