# Sea Otter Subspecies Classification :otter:

基于真实海獭形态学数据的二分类项目，目标是区分两个海獭亚种：

- **Enhydra lutris kenyoni**（Alaska）
- **Enhydra lutris nereis**（California）

项目重点不在于单一模型训练，而在于将两个字段体系不同、缺失情况明显、样本规模不一致的数据源整理为可比较的监督学习任务。

---

## 项目目标

- 对两份海獭捕获记录数据进行字段对齐与清洗
- 从形态学特征中筛选对亚种区分更有效的变量
- 比较多种分类模型在该任务上的表现
- 给出可解释的分类结果与实验结论

---

## 数据来源

项目使用两个公开数据集：

- `alaska_seaotter.csv`
- `california_seaotter.csv`

原始来源：

- Alaska: <https://www.sciencebase.gov/catalog/item/61a28ad0d34eb622f6974679>
- California: <https://www.sciencebase.gov/catalog/item/5d4b3de5e4b01d82ce8df3f3>

数据特征：

- 两个数据集字段命名方式不一致
- Alaska 数据中存在 `-9` 等占位值
- 缺失值较多
- 两类样本数量差异明显

---

## 方法概览

### 1. 数据对齐
将两个数据源中的对应字段映射为统一特征，包括：

- `weight`
- `length`
- `tail_length`
- `girth`
- `paw_width`
- `canine_width`

### 2. 数据处理
- 缺失值处理
- 异常占位值替换
- 幼体样本过滤
- 类别样本平衡

### 3. 特征选择
结合分布分析、缺失情况与可解释性，建模阶段重点使用：

- `weight`
- `paw_width`
- `canine_width`

### 4. 模型比较
项目比较了以下模型：

- Logistic Regression
- SVM
- Decision Tree
- Random Forest
- MLP

评估指标包括：

- Accuracy
- F1-score
- Precision
- Recall

---

## 运行环境

- Python 3
- Jupyter Notebook / Google Colab

主要依赖：

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

---

## 文件结构

```text
otter_classification/
├─ 24209702_OtterClassification.ipynb
├─ alaska_seaotter.csv
├─ california_seaotter.csv
├─ README_CN.md
├─ README.md
└─ dataset/
   ├─ alaska_seaotter.csv
   ├─ california_seaotter.csv
   └─ datafile.md
```

说明：

- `24209702_OtterClassification.ipynb`：项目主分析文件
- `alaska_seaotter.csv`：阿拉斯加海獭数据
- `california_seaotter.csv`：加州海獭数据
- `dataset/`：当前包含同名数据副本

---

## 主要结论

- 海獭亚种之间存在可被模型识别的形态学差异
- 在本项目比较的模型中，**Random Forest** 表现最稳定
- notebook 中可见结果显示：
  - 一轮实验中 Random Forest Accuracy 约为 `0.874`
  - 在进一步清洗与重采样后，调参版 Random Forest 达到：
    - Accuracy `0.867`
    - F1-score `0.867`
    - Precision `0.867`
    - Recall `0.867`

---

## 项目价值

该项目展示了一个完整的数据建模流程：

- 异构数据源对齐
- 真实数据清洗
- 特征筛选
- 多模型比较
- 基于结果做模型选择

适合作为以 **tabular data classification**、**data preprocessing** 和 **applied machine learning** 为核心的项目展示。
