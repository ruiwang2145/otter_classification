"""Reproduce the notebook's final model, and report honest performance metrics.

Run from the repository root:
    python verification/verify_pipeline.py

The first block reproduces the 0.867 quoted in the README exactly. The later blocks
show why that number should be quoted as ~0.82 instead.
"""
import os
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURES = ["weight", "paw_width", "canine_width"]

COLUMNS = {
    "weight": ("Weight (kg)", "WEIGHT"),
    "length": ("Length (cm)", "true_standard_lgth"),
    "tail_length": ("Tail Length (cm)", "mean_tail_lgth"),
    "girth": ("Girth (cm)", "mean_girth"),
    "paw_width": ("Right paw width (mm)", "PAW"),
    "canine_width": ("Canine width (mm)", "CAN_DIA"),
}


def load_data():
    """Load both sources and build the cleaned, balanced modelling table."""
    north = pd.read_csv(os.path.join(ROOT, "alaska_seaotter.csv"), encoding="latin1")
    south = pd.read_csv(os.path.join(ROOT, "california_seaotter.csv"), encoding="latin1")
    north = north.rename(columns={north.columns[0]: "OTTER_NO"})

    # The Alaska file uses -9 as a missing-value placeholder.
    north = north.replace(-9, np.nan)

    # Keep adults only. Note the two files define adulthood differently.
    north_adults = north[north["AGE_CATEGORY"] != 0.0].dropna(subset=["AGE_CATEGORY"])
    south_adults = south[south["Age Estimate"] >= 1].dropna(subset=["Age Estimate"])

    south_clean = south_adults[[c[0] for c in COLUMNS.values()]].copy()
    south_clean.columns = list(COLUMNS)
    south_clean["subspecies"] = "nereis"

    north_clean = north_adults[[c[1] for c in COLUMNS.values()]].copy()
    north_clean.columns = list(COLUMNS)
    north_clean["subspecies"] = "kenyoni"

    south_clean = south_clean.dropna()
    north_clean = north_clean.dropna()

    # Balance the classes by down-sampling the majority class.
    k = min(len(south_clean), len(north_clean))
    pooled = pd.concat(
        [
            south_clean.sample(k, random_state=42),
            north_clean.sample(k, random_state=42),
        ],
        ignore_index=True,
    )
    return north, south, pooled, k, len(south_clean), len(north_clean)


def main():
    north, south, pooled, k, n_south, n_north = load_data()

    print("=" * 74)
    print("SAMPLE BUDGET")
    print("=" * 74)
    print("Alaska     raw rows                       : %5d" % len(north))
    print("           adults only (AGE_CATEGORY != 0): %5d" % len(north[north.AGE_CATEGORY != 0.0].dropna(subset=["AGE_CATEGORY"])))
    print("           all 3 features present         : %5d" % n_north)
    print("California raw rows                       : %5d" % len(south))
    print("           adults only (Age Estimate >= 1): %5d" % len(south[south["Age Estimate"] >= 1].dropna(subset=["Age Estimate"])))
    print("           all 3 features present         : %5d" % n_south)
    print("Balanced pooled dataset                   : %5d  (%d per class)" % (2 * k, k))
    print("  -> %d usable Alaska adult records (%.0f%%) were discarded to force balance"
          % (n_north - k, 100 * (n_north - k) / n_north))

    data = pooled[FEATURES + ["subspecies"]].dropna().copy()
    encoder = LabelEncoder()
    data["label"] = encoder.fit_transform(data["subspecies"])
    X, y = data[FEATURES], data["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print()
    print("=" * 74)
    print("EXACT REPRODUCTION OF THE NOTEBOOK'S HEADLINE")
    print("=" * 74)
    print("train/test split: %d / %d rows" % (len(X_train), len(X_test)))
    for seed in (42, 0):
        model = RandomForestClassifier(n_estimators=100, random_state=seed).fit(X_train, y_train)
        pred = model.predict(X_test)
        print("  random_state=%-5s -> accuracy %.6f  F1 %.6f  (%d/%d correct)"
              % (seed, accuracy_score(y_test, pred), f1_score(y_test, pred),
                 int((pred == y_test).sum()), len(y_test)))
    print("  The notebook stored 0.867 for random_state=42, i.e. 52 of 60 test rows.")
    print("  Note how much the same split moves just by changing the model's own seed.")

    print()
    print("=" * 74)
    print("HOW STABLE IS THAT NUMBER?")
    print("=" * 74)
    scores = []
    for seed in range(400):
        a, b, c, d = train_test_split(X, y, test_size=0.2, stratify=y, random_state=seed)
        scores.append(
            accuracy_score(d, RandomForestClassifier(n_estimators=100, random_state=42).fit(a, c).predict(b))
        )
    scores = np.array(scores)
    print("400 random 80/20 splits : mean %.3f  sd %.3f  5th-95th pct [%.3f, %.3f]"
          % (scores.mean(), scores.std(), np.percentile(scores, 5), np.percentile(scores, 95)))
    print("seed 42 landed at the %.0fth percentile of that distribution"
          % (100 * (scores < 0.867).mean()))

    cv = StratifiedKFold(5, shuffle=True, random_state=42)
    acc = cross_val_score(RandomForestClassifier(n_estimators=100, random_state=42), X, y,
                          cv=cv, scoring="accuracy")
    f1 = cross_val_score(RandomForestClassifier(n_estimators=100, random_state=42), X, y,
                         cv=cv, scoring="f1")
    print("5-fold CV accuracy      : %.3f +- %.3f   (folds %s)" % (acc.mean(), acc.std(), np.round(acc, 3)))
    print("5-fold CV F1            : %.3f +- %.3f" % (f1.mean(), f1.std()))
    print()
    print("Conclusion: quote the result as ~0.82 (5-fold CV). The 0.867 single-split figure")
    print("rests on 60 test observations and is a favourable draw.")


if __name__ == "__main__":
    main()
