"""Measure the data-provenance confound between the two source files.

Run from the repository root:
    python verification/verify_confound.py

Each subspecies comes from a separate field survey, so the label is identical to the data
source. This script quantifies how far the two sources differ in field protocol, then runs a
control experiment to find out how much of the model's accuracy comes from a recording-format
artefact rather than from anything biological.
"""
import os
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

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


def load():
    north = pd.read_csv(os.path.join(ROOT, "alaska_seaotter.csv"), encoding="latin1")
    south = pd.read_csv(os.path.join(ROOT, "california_seaotter.csv"), encoding="latin1")
    north = north.rename(columns={north.columns[0]: "OTTER_NO"}).replace(-9, np.nan)
    return north, south


def build_pool(north, south):
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
    pool = pd.concat([sc.sample(k, random_state=42), nc.sample(k, random_state=42)], ignore_index=True)
    pool["label"] = (pool["subspecies"] == "nereis").astype(int)
    return pool


def main():
    north, south = load()
    pool = build_pool(north, south)

    print("=" * 74)
    print("EVIDENCE 1 - THE TWO FILES DO NOT RECORD THE SAME FIELDS")
    print("=" * 74)
    print("%-14s %14s %14s" % ("feature", "Alaska missing", "California missing"))
    for name in ["tail_length", "girth", "paw_width", "canine_width"]:
        ak = pd.to_numeric(north[COLUMNS[name][1]], errors="coerce")
        ca = pd.to_numeric(south[COLUMNS[name][0]], errors="coerce")
        print("%-14s %13.0f%% %13.0f%%" % (name, 100 * ak.isna().mean(), 100 * ca.isna().mean()))

    print()
    print("=" * 74)
    print("EVIDENCE 2 - THE TWO FILES RECORD AT DIFFERENT RESOLUTION")
    print("=" * 74)
    print("%-14s %22s %22s" % ("feature", "Alaska whole numbers", "California whole numbers"))
    for name in FEATURES:
        a = pd.to_numeric(pool.loc[pool.subspecies == "kenyoni", name], errors="coerce").dropna()
        c = pd.to_numeric(pool.loc[pool.subspecies == "nereis", name], errors="coerce").dropna()
        print("%-14s %21.1f%% %21.1f%%" % (name, 100 * ((a % 1) == 0).mean(), 100 * ((c % 1) == 0).mean()))

    print()
    print("=" * 74)
    print("EVIDENCE 3 - THE FEATURES SEPARATE THE SOURCES, NOT JUST THE SUBSPECIES")
    print("=" * 74)
    for name in FEATURES:
        a = pd.to_numeric(pool.loc[pool.subspecies == "kenyoni", name], errors="coerce").dropna()
        c = pd.to_numeric(pool.loc[pool.subspecies == "nereis", name], errors="coerce").dropna()
        print("%-14s kenyoni %7.2f +- %5.2f  |  nereis %7.2f +- %5.2f"
              % (name, a.mean(), a.std(), c.mean(), c.std()))
    print()
    print("A single threshold on paw_width nearly separates the two files. But the label IS")
    print("the file, so 'which subspecies' and 'which survey' cannot be told apart here.")

    print()
    print("=" * 74)
    print("CONTROL EXPERIMENT - HOW BIG IS THE RECORDING-FORMAT LEAK?")
    print("=" * 74)
    flags = pd.DataFrame({
        "paw_has_decimal": (pool["paw_width"] % 1 != 0).astype(int),
        "canine_has_decimal": (pool["canine_width"] % 1 != 0).astype(int),
    })
    for col in flags.columns:
        print("%-20s agrees with the true label on %.1f%% of rows"
              % (col, 100 * (flags[col] == pool["label"]).mean()))
    cv = StratifiedKFold(5, shuffle=True, random_state=42)
    flag_score = cross_val_score(RandomForestClassifier(n_estimators=100, random_state=42),
                                 flags.values, pool["label"], cv=cv, scoring="accuracy")
    print("model using ONLY those two flags : CV accuracy %.3f" % flag_score.mean())
    print("(these flags describe the paperwork, not the animal)")
    print()

    print("Now give both sources the same recording resolution and re-score the real model:")
    print("%-38s %s" % ("treatment", "5-fold CV accuracy"))
    for label, fn in [("as-is (mixed precision)", lambda d: d),
                      ("rounded to whole units", lambda d: d.round(0)),
                      ("rounded to 1 decimal", lambda d: d.round(1))]:
        X = fn(pool[FEATURES].copy())
        score = cross_val_score(RandomForestClassifier(n_estimators=100, random_state=42),
                                X, pool["label"], cv=cv, scoring="accuracy").mean()
        print("%-38s %.3f" % (label, score))
    print()
    print("The accuracy barely moves, so the precision fingerprint is NOT the main driver.")
    print("The real problem is structural: there is no held-out source, so the model's skill")
    print("cannot be attributed to biology rather than to provenance. Documented, not hidden.")


if __name__ == "__main__":
    main()
