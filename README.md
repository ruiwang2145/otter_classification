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
- [Confounds & Limitations](#-confounds--limitations)
- [Installation & Usage](#-installation--usage)
- [Dependencies](#-dependencies)
- [Future Work](#-future-work)
- [Reproducing the Results](#-reproducing-the-results)
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
├── dataset/
│   ├── alaska_seaotter.csv             # Dataset copy (Alaska)
│   ├── california_seaotter.csv         # Dataset copy (California)
│   └── datafile.md                     # Field mapping, missing-value and age conventions
└── verification/
    ├── verify_pipeline.py              # Reproduces the headline model + honest metrics
    ├── verify_rounds.py                # Round 1 vs Round 2 comparison
    └── verify_confound.py              # Quantifies the data-provenance confound
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
| **Placeholder removal** | Replaced `-9` with `NaN` in the Alaska dataset |
| **Juvenile filtering** | Applied *after* the first round of modelling, using each source's own age field: `AGE_CATEGORY != 0` (Alaska) and `Age Estimate >= 1` (California). Note these two rules do not select the same life stage — see [Confounds & Limitations](#-confounds--limitations). |
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

All metrics below are copied verbatim from the notebook's stored cell outputs, so they can be
verified by re-running the notebook. **Round 1** = pooled data before the juvenile filter and
class balancing; **Round 2** = final model after both.

**Round 1 — pooled data, no juvenile filter, no balancing (866 rows, 17% minority class)**

| Model | Accuracy | F1-score (weighted) |
|---|---|---|
| Logistic Regression | 0.8333 | 0.8177 |
| SVM (RBF) | 0.8276 | 0.7598 |
| Decision Tree | 0.8448 | 0.8364 |
| **Random Forest** | **0.8736** | **0.8630** |
| Neural Network (MLP) | 0.8391 | 0.7758 |

> ⚠️ These round-1 accuracy figures look healthy, but the per-class metrics do not. On the
> same split, Random Forest reached accuracy 0.879 while **F1 was only 0.553 and recall on the
> minority class was 0.433** — more than half of the California otters were missed. Accuracy was
> being carried by the 83% majority class. This is what triggered the error analysis in §3.3.

**Round 2 — final model: adults only, classes balanced to 148 / 148 (296 rows)**

| Metric | Value |
|---|---|
| **Algorithm** | Random Forest (100 estimators, GridSearchCV-tuned) |
| **Accuracy (single 80/20 split, seed 42, 60 test rows)** | **0.867** |
| **Accuracy (5-fold stratified CV)** | **0.824 ± 0.051** |
| **F1 (5-fold stratified CV)** | **0.820 ± 0.052** |
| **Accuracy (mean of 400 random 80/20 splits)** | **0.819 ± 0.046** |

> The 0.867 headline comes from a single split with only **60 test observations** — 52 correct.
> It is fully reproducible (`random_state=42`), but reporting three decimals on 60 samples is
> false precision. Across 400 random splits the result is 0.819 ± 0.046 (5th–95th percentile
> 0.750–0.883), and 5-fold CV gives 0.824. **Quote it as ~0.82.**

### The Effect of the Data Fix (same model, 200 random splits each)

This is the result the project is really about. Accuracy barely moved — but it was never the
metric that mattered.

| | Round 1 (raw pooled data) | Round 2 (adults only + balanced) |
|---|---|---|
| Rows | 866 | 296 |
| Minority class share | 17% | 50% |
| **Accuracy** | **0.866 ± 0.018** | 0.817 ± 0.045 |
| **F1** | **0.543 ± 0.069** | **0.813 ± 0.050** |
| **Minority-class recall** | **0.468 ± 0.083** | **0.801 ± 0.079** |
| Precision | 0.660 ± 0.078 | 0.832 ± 0.058 |

Accuracy *fell* while F1 rose by 50% and minority-class recall nearly doubled. The takeaway is
not "the model got more accurate" — it is that **accuracy was hiding a model that failed on
half of one class**, and the fix was in the data, not the algorithm.

### Key Findings

- 🧬 **The two sources are cleanly separable on these measurements** — but see [Confounds & Limitations](#-confounds--limitations): because each subspecies comes from a different survey, this cannot be attributed to biology alone.
- 📏 **Weight is the strongest feature**: Aligns with biological expectation — northern otters are larger.
- 🦷 **Canine width adds discriminative power**: Supports documented jaw morphology differences.
- 📉 **Accuracy was a misleading metric here**: with a 17% minority class, the round-1 model showed accuracy 0.87 while missing more than half of the minority class (recall 0.47, F1 0.54). Fixing the data — not the model — moved F1 to 0.81 and recall to 0.80.
- 🧒 **Removing juveniles and balancing the classes improved generalisation**: but note that this is *not* because the misclassified animals were juveniles (see below) — it is because immature morphology is genuinely unstable and the class imbalance was distorting the metrics.
- 🌲 **Random Forest wins**: Best balance of accuracy, F1-score, and interpretability across all tested models.
- ⚠️ **~18% misclassification rate remains** (5-fold CV accuracy 0.824). The model should be used as a decision-support tool, not a replacement for expert judgment.

### What the Misclassified Animals Actually Were

The notebook's error analysis (§3.3) states that the misclassified individuals "exhibited
characteristics typical of juvenile sea otters". Printing the actual misclassified rows from
the final model does **not** support that attribution — every error was an adult in the
morphometric overlap zone between the two subspecies:

| weight (kg) | paw_width (mm) | canine_width (mm) | true | predicted |
|---|---|---|---|---|
| 17.00 | 45.8 | 8.00 | kenyoni | nereis |
| 28.30 | 43.8 | 7.73 | nereis | kenyoni |
| 26.76 | 43.5 | 7.90 | nereis | kenyoni |
| 21.40 | 48.5 | 7.80 | nereis | kenyoni |
| 26.76 | 48.6 | 8.10 | nereis | kenyoni |
| 17.50 | 47.0 | 7.70 | kenyoni | nereis |
| 17.20 | 43.3 | 6.70 | kenyoni | nereis |
| 29.00 | 49.1 | 8.30 | kenyoni | nereis |
| 22.70 | 40.5 | 7.00 | kenyoni | nereis |

The **action** taken (removing pups, balancing classes) was correct and did fix the metric
problem — the **stated reason** was not. The honest explanation is that the errors sit where the
two subspecies genuinely overlap, and that the round-1 metric was dominated by class imbalance.

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

## 🔬 Confounds & Limitations

### The label and the data source are the same variable

This is the single most important caveat in the project. Each subspecies comes from a
**separate field survey** (Alaska and California), so "which subspecies is this?" and "which
survey measured this otter?" are **the same question**. Any systematic difference between the
two surveys is therefore indistinguishable from a biological difference — and the two files do
differ systematically:

**Different field protocols (share of rows missing each measurement):**

| Feature | Alaska | California |
|---|---|---|
| `tail_length` | **91%** missing | **1%** missing |
| `paw_width` | **83%** missing | **5%** missing |
| `girth` | **77%** missing | **5%** missing |
| `canine_width` | **75%** missing | **20%** missing |

**Different recording resolution (share of values recorded as whole numbers):**

| Feature | Alaska | California |
|---|---|---|
| `paw_width` | **30.4%** | **10.1%** |

**Different "adult" definitions:** the Alaska filter (`AGE_CATEGORY != 0`) keeps animals aged
1.5 years, while the California filter (`Age Estimate >= 1`) keeps animals aged 1 year. Sea
otters mature around 3–5 years, so both rules admit sub-adults — but not the *same* sub-adults.

### How large is the recording-precision leak?

To avoid over-claiming, this was measured with a control experiment rather than asserted:

| Treatment | 5-fold CV accuracy |
|---|---|
| As-is (mixed precision across sources) | 0.824 |
| Both sources rounded to whole units | 0.808 |
| Both sources rounded to 1 decimal | 0.797 |

A model trained on **nothing but two "does this value have decimals" flags** reaches only
**0.601** CV accuracy. So the precision fingerprint is real but is **not** the main driver —
the separation survives uniform rounding. The problem is more fundamental: **no held-out
source exists**, so there is no way to demonstrate that the model learned biology rather than
provenance.

### What can and cannot be claimed

- ✅ **Can claim:** the pipeline is correct end-to-end; the direction of every feature
  difference is consistent with the published literature (Timm-Davis et al. 2015; Wilson et al.
  1991); the metrics are honestly reported.
- ❌ **Cannot claim:** that the two subspecies are demonstrably distinguishable by these
  measurements. That would require external validation on a source the model has never seen.

### Other limitations

- Only **3 features** used — `tail_length` and `girth` excluded due to missing data (91% / 77% in the Alaska file)
- Down-sampling discarded **143 of 291** usable Alaska adult records (49%). Retaining all rows with `class_weight='balanced'` would be a better design.
- Only **296 rows** survive cleaning, so the 0.867 single-split figure rests on a **60-row test set**
- Results are reported from repeated splits and 5-fold CV, but still from a single pooled dataset

## 🚧 Future Work

- [ ] Obtain a **held-out source** (a third survey, or time-separated captures) to test whether the signal is biological rather than provenance-driven
- [ ] Retain all rows and use `class_weight='balanced'` instead of down-sampling
- [ ] Incorporate additional features with better imputation strategies (e.g., MICE, KNN imputation)
- [ ] Explore gradient boosting models (XGBoost, LightGBM, CatBoost)
- [ ] Apply **SHAP** for instance-level interpretability
- [ ] Add stratified k-fold metrics and confidence intervals as standard reporting
- [ ] Publish a more comprehensive feature engineering pipeline

---

## 🔁 Reproducing the Results

Every number quoted in this README can be regenerated from the raw CSVs. The
`verification/` folder contains standalone scripts that re-run the whole analysis
independently of the notebook:

| Script | What it checks |
|---|---|
| `verification/verify_pipeline.py` | Reproduces the notebook's final model exactly, and reports repeated-split and 5-fold CV metrics |
| `verification/verify_rounds.py` | The Round 1 vs Round 2 comparison (200 random splits each) and the sample-loss budget |
| `verification/verify_confound.py` | Missingness and recording-resolution differences between the two sources, plus the uniform-precision control experiment |

```bash
pip install pandas numpy scikit-learn
python verification/verify_pipeline.py
python verification/verify_rounds.py
python verification/verify_confound.py
```

Expected headline output:

```
total=296 train=236 test=60
random_state=42    -> accuracy 0.866667  F1 0.866667  (52/60 correct)   <- the README's 0.867
random_state=0     -> accuracy 0.816667  F1 0.825397  (49/60 correct)
400 random 80/20 splits : mean 0.819  sd 0.046  5th-95th pct [0.750, 0.883]
5-fold CV accuracy      : 0.824 +- 0.051
```

---

## 🙏 Acknowledgements

This project was inspired by the **Palmer Penguins** dataset project by Dr. Allison Horst ([github.com/allisonhorst/palmerpenguins](https://github.com/allisonhorst/palmerpenguins)), which demonstrated the elegant use of body measurements to classify biological categories.

Scientific references:
- Timm-Davis, L. L., DeWitt, T. J., & Marshall, C. D. (2015). *Divergent skull morphology supports two trophic specializations in otters (Lutrinae).* PLoS ONE, 10(12), e0143236.
- Wilson, D. E., Bogan, M. A., Brownell, R. L., Burdin, A. M., & Maminov, M. K. (1991). *Geographic Variation in Sea Otters, Enhydra lutris.* Journal of Mammalogy, 72(1), 22–36.
