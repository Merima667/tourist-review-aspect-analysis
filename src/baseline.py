"""
Baseline: TF-IDF + logistic regression.

Two parts, as described in the proposal:
1. Aspect detection: one binary classifier per aspect (is the aspect mentioned or not?).
2. Aspect sentiment: one classifier that predicts positive / negative / neutral
   for an aspect that is mentioned. The aspect name is added to the text as an
   extra token (e.g. "__staff__ konobar je bio ljubazan"), so one model can learn
   all four aspects.

The model is trained only on English (en_train), tuned on en_val, and tested
on English, Turkish and Bosnian without retraining (zero-shot).

Results are saved to results/baseline/.
Run src/preprocess.py first. bs_test.csv is not in the repository
(see README, Bosnian test set); if it is missing, it is skipped.
"""
import os

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

SEED = 42
PROCESSED_DIR = os.path.join("data", "processed")
OUT_DIR = os.path.join("results", "baseline")

ASPECTS = ["food", "staff", "price", "location"]
SENTIMENTS = ["positive", "negative", "neutral"]  # conflict is not predicted
TEST_SETS = ["en_val", "en_test", "tr_test", "bs_test"]


def load(name):
    path = os.path.join(PROCESSED_DIR, f"{name}.csv")
    if not os.path.exists(path):
        return None
    return pd.read_csv(path, encoding="utf-8")


def make_vectorizer():
    # word unigrams + bigrams, lowercase; the same settings for both parts
    return TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2, sublinear_tf=True)


def sentiment_pairs(df):
    """One row per (sentence, mentioned aspect) with a sentiment label."""
    rows = []
    for _, r in df.iterrows():
        for a in ASPECTS:
            if r[a] in SENTIMENTS:
                rows.append({"text": f"__{a}__ {r['text']}", "aspect": a, "label": r[a]})
    return pd.DataFrame(rows)


def train(train_df):
    # 1. aspect detection
    det_vec = make_vectorizer()
    X = det_vec.fit_transform(train_df["text"])
    detectors = {}
    for a in ASPECTS:
        y = (train_df[a] != "none").astype(int)
        clf = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED)
        detectors[a] = clf.fit(X, y)

    # 2. aspect sentiment
    pairs = sentiment_pairs(train_df)
    sent_vec = make_vectorizer()
    Xs = sent_vec.fit_transform(pairs["text"])
    sent_clf = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED)
    sent_clf.fit(Xs, pairs["label"])
    return det_vec, detectors, sent_vec, sent_clf


def evaluate(df, name, domain, model):
    det_vec, detectors, sent_vec, sent_clf = model
    X = det_vec.transform(df["text"])

    # aspect detection: micro- and macro-F1 over the four aspects
    y_true = np.column_stack([(df[a] != "none").astype(int) for a in ASPECTS])
    y_pred = np.column_stack([detectors[a].predict(X) for a in ASPECTS])
    row = {"dataset": name, "domain": domain, "sentences": len(df),
           "aspect_micro_f1": f1_score(y_true, y_pred, average="micro", zero_division=0),
           "aspect_macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0)}
    for i, a in enumerate(ASPECTS):
        row[f"f1_{a}"] = f1_score(y_true[:, i], y_pred[:, i], zero_division=0)

    # aspect sentiment: evaluated on the gold aspects (conflict excluded)
    pairs = sentiment_pairs(df)
    if len(pairs):
        pred = sent_clf.predict(sent_vec.transform(pairs["text"]))
        row["sentiment_macro_f1"] = f1_score(pairs["label"], pred, labels=SENTIMENTS,
                                             average="macro", zero_division=0)
        row["sentiment_accuracy"] = accuracy_score(pairs["label"], pred)
        row["sentiment_pairs"] = len(pairs)
    return row


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    train_df = load("en_train")
    model = train(train_df)

    rows = []
    for name in TEST_SETS:
        df = load(name)
        if df is None:
            print(f"{name}.csv not found, skipped")
            continue
        rows.append(evaluate(df, name, "all", model))
        if name == "bs_test":  # restaurant vs hotel
            for dom in ["restaurant", "hotel"]:
                rows.append(evaluate(df[df["domain"] == dom], name, dom, model))

    results = pd.DataFrame(rows).round(3)
    results.to_csv(os.path.join(OUT_DIR, "baseline_results.csv"), index=False)
    pd.set_option("display.width", 200)
    print(results.to_string(index=False))
    print("\nSaved to", os.path.join(OUT_DIR, "baseline_results.csv"))


if __name__ == "__main__":
    main()
