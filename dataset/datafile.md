# Data Description Notes

Two public capture datasets from the United States Geological Survey (USGS), published via
ScienceBase. Each file covers a different sea otter subspecies, and they were produced by
**different field surveys** — which is the source of the confound documented in the main
README.

| Subspecies | Region | File | Source |
|---|---|---|---|
| *Enhydra lutris kenyoni* | Alaska (North) | `alaska_seaotter.csv` | <https://www.sciencebase.gov/catalog/item/61a28ad0d34eb622f6974679> |
| *Enhydra lutris nereis* | California (South) | `california_seaotter.csv` | <https://www.sciencebase.gov/catalog/item/5d4b3de5e4b01d82ce8df3f3> |

- Alaska: 4,478 rows × 49 columns
- California: 192 rows × 60 columns
- Both files are read with `encoding="latin1"`; the Alaska file has a UTF-8 BOM on the first column name.

## Field mapping used in the analysis

The two files name the same anatomical measurements differently. The mapping below is what the
notebook applies.

| Unified name | Alaska column | California column | Unit |
|---|---|---|---|
| `weight` | `WEIGHT` | `Weight (kg)` | kg |
| `length` | `true_standard_lgth` | `Length (cm)` | cm |
| `tail_length` | `mean_tail_lgth` | `Tail Length (cm)` | cm |
| `girth` | `mean_girth` | `Girth (cm)` | cm |
| `paw_width` | `PAW` | `Right paw width (mm)` | mm |
| `canine_width` | `CAN_DIA` | `Canine width (mm)` | mm |

Note that California also carries `Weight (lbs)`, which is **not** used — `Weight (kg)` is
taken instead to match the Alaska unit.

## Missing-value conventions

- **Alaska** uses `-9` as a missing-value placeholder. The notebook replaces `-9` with `NaN`
  across the whole Alaska frame. Missing counts for the six modelled fields:

  | Field | Missing (of 4,478) |
  |---|---|
  | `tail_length` | 91% |
  | `paw_width` | 83% |
  | `girth` | 77% |
  | `canine_width` | 75% |
  | `length` | 4% |
  | `weight` | <1% |

- **California** uses empty cells rather than a sentinel, and is far more complete:

  | Field | Missing (of 192) |
  |---|---|
  | `canine_width` | 20% |
  | `paw_width` | 5% |
  | `girth` | 5% |
  | `tail_length` | 1% |
  | `length` | 4% |
  | `weight` | 2% |

  Because of the different conventions, the two files disagree sharply on *which* measurements
  exist. See the "Confounds & Limitations" section of the main README.

## Age fields — and why they are not equivalent

| | Alaska | California |
|---|---|---|
| Column | `AGE_CATEGORY` | `AgeClass` (letter code) and `Age Estimate` (years) |
| Values seen | `7`, `1.5`, `13`, `0`, `-9` | `a`/`s`/`o`/`p`/`j`; age 0.06–12 |
| Meaning of `0` | pup | — |
| Filter used in the notebook | `AGE_CATEGORY != 0` | `Age Estimate >= 1` |

`AGE_CATEGORY` is in fact an age in **years**, not a category code. Sea otters mature around
3–5 years, so the Alaska rule still admits 1.5-year-olds while the California rule admits
1-year-olds. The two "adult" filters therefore select different life stages — another
label-correlated difference between the two sources.

## Recording resolution

The two surveys recorded values to different precision, which is itself a fingerprint of the
source file:

| Field | Alaska recorded as whole numbers | California recorded as whole numbers |
|---|---|---|
| `paw_width` | 30.4% | 10.1% |
| `canine_width` | 14.2% | 15.5% |
| `weight` | 14.2% | 12.8% |

Quantifying this artefact is the purpose of `verification/verify_confound.py`.
