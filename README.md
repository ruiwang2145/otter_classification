# Sea Otter Subspecies Classification :otter:

A binary classification project based on real-world sea otter morphometric data, designed to distinguish between two subspecies:

- **Enhydra lutris kenyoni** (Alaska)
- **Enhydra lutris nereis** (California)

The project focuses on turning heterogeneous biological datasets into a comparable supervised learning task, rather than on model training alone.

---

## Project Objective

- align and clean two sea otter capture datasets
- identify morphometric features with stronger discriminative value
- compare multiple classification models on the same task
- produce interpretable experimental results

---

## Data Sources

The project uses two public datasets:

- `alaska_seaotter.csv`
- `california_seaotter.csv`

Original sources referenced in the notebook:

- Alaska: <https://www.sciencebase.gov/catalog/item/61a28ad0d34eb622f6974679>
- California: <https://www.sciencebase.gov/catalog/item/5d4b3de5e4b01d82ce8df3f3>

Key data characteristics:

- inconsistent column naming across sources
- placeholder values such as `-9` in the Alaska dataset
- substantial missingness
- strong sample size imbalance between the two classes

---

## Method Overview

### 1. Data Alignment
Equivalent fields from the two datasets are mapped into a unified feature space, including:

- `weight`
- `length`
- `tail_length`
- `girth`
- `paw_width`
- `canine_width`

### 2. Data Processing
- missing-value handling
- placeholder-value replacement
- juvenile sample filtering
- class balancing

### 3. Feature Selection
Based on data quality, distribution analysis, and interpretability, the final modeling stage emphasizes:

- `weight`
- `paw_width`
- `canine_width`

### 4. Model Comparison
The following models are compared:

- Logistic Regression
- SVM
- Decision Tree
- Random Forest
- MLP

Evaluation metrics include:

- Accuracy
- F1-score
- Precision
- Recall

---

## Runtime Environment

- Python 3
- Jupyter Notebook / Google Colab

Main dependencies:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

---

## File Structure

```text
otter_classification/
├─ 24209702_OtterClassification.ipynb
├─ alaska_seaotter.csv
├─ california_seaotter.csv
├─ README.md
├─ README_EN.md
└─ dataset/
   ├─ alaska_seaotter.csv
   ├─ california_seaotter.csv
   └─ datafile.md
```

Notes:

- `24209702_OtterClassification.ipynb`: main analysis notebook
- `alaska_seaotter.csv`: Alaska sea otter dataset
- `california_seaotter.csv`: California sea otter dataset
- `dataset/`: currently contains duplicate copies of the CSV files

---

## Main Results

- the two subspecies show measurable morphometric differences that can be captured by classification models
- among the tested models, **Random Forest** provides the strongest overall performance
- results visible in the notebook include:
  - Random Forest accuracy of approximately `0.874` in one experiment
  - after stricter cleaning and resampling, tuned Random Forest reaches:
    - Accuracy `0.867`
    - F1-score `0.867`
    - Precision `0.867`
    - Recall `0.867`

---

## Project Value

This project demonstrates a complete applied machine learning workflow for tabular data:

- heterogeneous data alignment
- real-world data cleaning
- feature selection
- multi-model comparison
- evidence-based model choice

It is well suited for portfolio presentation in areas related to **tabular classification**, **data preprocessing**, and **applied machine learning**.
