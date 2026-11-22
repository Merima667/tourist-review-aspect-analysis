"""
Inter-annotator agreement (Cohen's kappa) for the Bosnian test set.

Two annotators labelled the same 50 randomly selected reviews (213 sentences)
independently. This script compares their ORIGINAL files (before the
disagreements were resolved) and prints observed agreement and Cohen's kappa
per aspect. Results are saved to results/kappa/kappa.csv.

The annotation files contain the review texts, so they are not in the
repository. Put them in data/annotation/ before running:
    data/annotation/kappa_annotator_1.xlsx
    data/annotation/kappa_annotator_2.xlsx
"""
import os

import pandas as pd
from sklearn.metrics import cohen_kappa_score

ASPECTS = ["food", "staff", "price", "location"]
FILE_1 = os.path.join("data", "annotation", "kappa_annotator_1.xlsx")
FILE_2 = os.path.join("data", "annotation", "kappa_annotator_2.xlsx")
OUT_DIR = os.path.join("results", "kappa")


def main():
    a = pd.read_excel(FILE_1, sheet_name="Anotacija").set_index("sentence_id")
    b = pd.read_excel(FILE_2, sheet_name="Anotacija").set_index("sentence_id")
    b = b.loc[a.index]  # same sentence order

    rows = []
    for aspect in ASPECTS:
        x = a[aspect].fillna("none").str.strip()
        y = b[aspect].fillna("none").str.strip()
        rows.append({"aspect": aspect,
                     "observed_agreement": (x == y).mean(),
                     "cohen_kappa": cohen_kappa_score(x, y)})
    res = pd.DataFrame(rows)
    res.loc[len(res)] = ["average", res["observed_agreement"].mean(), res["cohen_kappa"].mean()]
    res = res.round(3)

    os.makedirs(OUT_DIR, exist_ok=True)
    res.to_csv(os.path.join(OUT_DIR, "kappa.csv"), index=False)
    print(f"Sentences: {len(a)}")
    print(res.to_string(index=False))


if __name__ == "__main__":
    main()
