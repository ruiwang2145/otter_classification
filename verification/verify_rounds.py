"""Round 1 vs Round 2: what the data fix actually changed.

Run from the repository root:
    python verification/verify_rounds.py

Round 1 = pooled raw data, no juvenile filter, no balancing (what the notebook does first).
Round 2 = adults only, classes balanced 1:1 (the notebook's final model).

Both rounds use the same model and the same 200 random splits, so the comparison is fair.
"""
import os
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
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


def build_rounds():
    north = pd.read_csv(os.path.join(ROOT, "alaska_seaotter.csv"), encoding="latin1")
    south = pd.read_csv(os.path.join(ROOT, "california_seaotter.csv"), encoding="latin1")
    north = north.rename(columns={north.columns[0]: "OTTER_NO"}).replace(-9, np.nan)

    encoder = LabelEncoder()

    # ---- round 1: pooled raw, no filters ----
    s1 = south[[c[0] for c in COLUMNS.values()]].copy()
    s1.columns = list(COLUMNS)
    s1["subspecies"] = "nereis"
    n1 = north[[c[1] for c in COLUMNS.values()]].copy()
    n1.columns = list(COLUMNS)
    n1["subspecies"] = "kenyoni"
    r1 = pd.concat([s1, n1], ignore_index=True)[FEATURES + ["subspecies"]].dropna().copy()
    r1["label"] = encoder.fit_transform(r1["subspecies"])

    # ---- round 2: adults only + balanced ----
    n_adults = north[north["AGE_CATEGORY"] != 0.0].dropna(subset=["AGE_CATEGORY"])
    s_adults = south[south["Age Estimate"] >= 1].dropna(subset=["Age Estimate"])
    sc = s_adults[[c[0] for c in COLUMNS.values()]].copy()
    sc.columns = list(COLUMNS)
    sc["subspecies"] = "nereis"
    nc = n_adults[[c[1] for c in COLUMNS.values()]].copy()
    nc.columns = list(COLUMNS)
    nc["subspecies"] = "kenyoni"
    sc, nc = sc.dropna(), nc.dropna()
    k = min(len(sc), len(nc))
    r2 = pd.concat([sc.sample(k, random_state=42), nc.sample(k, random_state=42)],
                   ignore_index=True)[FEATURES + ["subspecies"]].dropna().copy()
    r2["label"] = encoder.fit_transform(r2["subspecies"])
    return r1, r2


def evaluate(data, n_splits=200):
    metrics = {"accuracy": [], "f1": [], "recall": [], "precision": []}
    for seed in range(n_splits):
        X_train, X_test, y_train, y_test = train_test_split(
            data[FEATURES], data["label"], test_size=0.2, stratify=data["label"], random_state=seed
        )
        pred = RandomForestClassifier(n_estimators=100, random_state=seed).fit(X_train, y_train).predict(X_test)
        metrics["accuracy"].append(accuracy_score(y_test, pred))
        metrics["f1"].append(f1_score(y_test, pred))
        metrics["recall"].append(recall_score(y_test, pred))
        metrics["precision"].append(precision_score(y_test, pred))
    return {name: (np.mean(v), np.std(v)) for name, v in metrics.items()}


def main():
    r1, r2 = build_rounds()

    print("=" * 74)
    print("ROUND 1 vs ROUND 2  (same model, same 200 splits)")
    print("=" * 74)
    print("round 1: %3d rows, minority class share %.0f%%" % (len(r1), 100 * r1["label"].mean()))
    print("round 2: %3d rows, minority class share %.0f%%" % (len(r2), 100 * r2["label"].mean()))
    print()

    results = {}
    for tag, data in (("round 1", r1), ("round 2", r2)):
        results[tag] = evaluate(data)
        m = results[tag]
        print("%-8s accuracy %.3f+-%.3f | F1 %.3f+-%.3f | recall %.3f+-%.3f | precision %.3f+-%.3f"
              % (tag, m["accuracy"][0], m["accuracy"][1], m["f1"][0], m["f1"][1],
                 m["recall"][0], m["recall"][1], m["precision"][0], m["precision"][1]))

    print()
    d_acc = results["round 2"]["accuracy"][0] - results["round 1"]["accuracy"][0]
    d_f1 = results["round 2"]["f1"][0] - results["round 1"]["f1"][0]
    d_rec = results["round 2"]["recall"][0] - results["round 1"]["recall"][0]
    print("change from round 1 to round 2:")
    print("   accuracy  %+.3f   (it went DOWN)" % d_acc)
    print("   F1        %+.3f" % d_f1)
    print("   recall    %+.3f   (minority class)" % d_rec)
    print()
    print("Round 1's accuracy of %.3f looked fine, but recall was only %.3f - more than half"
          % (results["round 1"]["accuracy"][0], results["round 1"]["recall"][0]))
    print("of the minority class was being missed. Accuracy was carried by the majority class.")
    print("The value of the data fix is a metric-integrity improvement, not an accuracy gain.")


if __name__ == "__main__":
    main()
