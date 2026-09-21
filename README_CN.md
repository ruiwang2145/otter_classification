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
├─ dataset/
│  ├─ alaska_seaotter.csv
│  ├─ california_seaotter.csv
│  └─ datafile.md
└─ verification/
   ├─ verify_pipeline.py
   ├─ verify_rounds.py
   └─ verify_confound.py
```

说明：

- `24209702_OtterClassification.ipynb`：项目主分析文件
- `alaska_seaotter.csv`：阿拉斯加海獭数据
- `california_seaotter.csv`：加州海獭数据
- `dataset/`：当前包含同名数据副本，以及字段映射与缺失值约定说明
- `verification/`：独立复现脚本，不依赖 notebook 即可重跑全部结论

---

## 主要结论

- 海獭亚种之间存在可被模型识别的形态学差异（**但受下方「重要限制」约束**）
- 在本项目比较的模型中，**Random Forest** 表现最稳定
- notebook 中可见结果显示：
  - 一轮实验中 Random Forest Accuracy 约为 `0.874`
  - 在进一步清洗与重采样后，调参版 Random Forest 达到：
    - Accuracy `0.867`
    - F1-score `0.867`
    - Precision `0.867`
    - Recall `0.867`

> ⚠️ 上述 `0.867` 来自**单次 80/20 切分，测试集只有 60 条样本**（正确 52 条），可以用
> `random_state=42` 精确复现。但在 60 条样本上报三位小数属于虚假精度：400 次随机切分的
> 均值是 **0.819 ± 0.046**，5 折交叉验证是 **0.824 ± 0.051**。对外应报 **约 0.82**。

### 真正重要的结果：数据修正改变了什么

第一轮（未做幼体过滤、未平衡类别）的准确率 0.866 看起来正常，但 **F1 只有 0.543、
少数类召回率只有 0.468**——超过一半的加州海獭被漏判，准确率完全由占 83% 的多数类撑起。

| | 第一轮（原始合并数据） | 第二轮（仅成年体 + 类别平衡） |
|---|---|---|
| 样本量 | 866 | 296 |
| 少数类占比 | 17% | 50% |
| **准确率** | **0.866 ± 0.018** | 0.817 ± 0.045 |
| **F1** | **0.543 ± 0.069** | **0.813 ± 0.050** |
| **少数类召回率** | **0.468 ± 0.083** | **0.801 ± 0.079** |

准确率**下降**，但 F1 提升 50%、少数类召回率接近翻倍。这个项目真正的收获不是「模型更准了」，
而是**发现准确率掩盖了模型在一半类别上的失败**，而修正发生在数据层，不在算法层。

---

## 重要限制：标签与数据来源完全重合

这是本项目最关键的一条限制。两个亚种各来自**一次独立的野外调查**，因此
「这是哪个亚种」和「这条数据来自哪次调查」在数据里是**同一个问题**。两份文件在多个
维度上系统性地不同：

**记录的字段不同（缺失率）：**

| 特征 | 阿拉斯加 | 加州 |
|---|---|---|
| `tail_length` | **91%** 缺失 | **1%** 缺失 |
| `paw_width` | **83%** 缺失 | **5%** 缺失 |
| `girth` | **77%** 缺失 | **5%** 缺失 |
| `canine_width` | **75%** 缺失 | **20%** 缺失 |

**记录精度不同（记成整数的比例）：**

| 特征 | 阿拉斯加 | 加州 |
|---|---|---|
| `paw_width` | **30.4%** | **10.1%** |

**「成年」的定义不同**：阿拉斯加的过滤条件 `AGE_CATEGORY != 0` 会保留 1.5 岁的个体，
加州的 `Age Estimate >= 1` 保留 1 岁以上的个体。海獭约 3–5 岁性成熟，所以两边的
「成年」并不是同一批个体。

**这个泄漏有多大？** 用对照实验量化（而非主观断言）：

| 处理方式 | 5 折 CV 准确率 |
|---|---|
| 原样（两边精度混合） | 0.824 |
| 两边都四舍五入到整数 | 0.808 |
| 两边都保留一位小数 | 0.797 |

只用「这个值有没有小数」两个标志建模，交叉验证准确率只有 **0.601**。所以记录格式的泄漏
**确实存在，但不是主因**——统一精度后准确率几乎不掉。真正的问题是结构性的：
**没有留出（held-out）来源**，因此无法证明模型学到的是生物学差异而不是来源差异。

**因此：**

- ✅ **可以主张**：整条流水线是正确的；所有特征差异的方向都与已发表文献
  （Timm-Davis et al. 2015；Wilson et al. 1991）一致；指标是诚实报告的。
- ❌ **不能主张**：这两个亚种已被证明可以通过形态学测量区分。那需要在一个模型从未见过的
  独立数据源上做外部验证。

---

## 结果复现

`verification/` 目录下的脚本可在不打开 notebook 的情况下独立重跑全部结论：

| 脚本 | 作用 |
|---|---|
| `verification/verify_pipeline.py` | 精确复现最终模型，并输出重复切分与 5 折交叉验证指标 |
| `verification/verify_rounds.py` | 第一轮 vs 第二轮对照（各 200 次切分）与样本损耗账 |
| `verification/verify_confound.py` | 两个数据源的缺失率/记录精度差异，以及统一精度的对照实验 |

```bash
pip install pandas numpy scikit-learn
python verification/verify_pipeline.py
python verification/verify_rounds.py
python verification/verify_confound.py
```

---

## 项目价值

该项目展示了一个完整的数据建模流程：

- 异构数据源对齐
- 真实数据清洗
- 特征筛选
- 多模型比较
- 基于结果做模型选择
- **发现指标失效并修正（准确率 → F1 / 召回率）**
- **量化并明确写出结论的边界**

适合作为以 **tabular data classification**、**data preprocessing**、
**applied machine learning** 和 **metric integrity / root-cause analysis** 为核心的项目展示。
