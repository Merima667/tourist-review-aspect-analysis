"""
Preprocesses SemEval-2016 Task 5 restaurant data.

Steps:
1. Read the XML files from data/raw/.
2. Clean the text (keeps Bosnian and Turkish letters such as č, ć, š, ž, đ, ş, ğ).
3. Map SemEval categories to our four aspects: food, staff, price, location.
4. Split the English training data into train and validation sets (by review).
5. Save the results as CSV files in data/processed/.
"""
import os
import random
import re
import unicodedata
import xml.etree.ElementTree as ET

import pandas as pd

RAW_DIR = os.path.join("data", "raw")
OUT_DIR = os.path.join("data", "processed")

SEED = 42         # fixed seed, so the split is always the same    
VAL_RATIO = 0.1      

ASPECTS = ["food", "staff", "price", "location"]

CATEGORY_MAP = {
    "FOOD#QUALITY": "food",
    "FOOD#STYLE_OPTIONS": "food",
    "DRINKS#QUALITY": "food",
    "DRINKS#STYLE_OPTIONS": "food",
    "SERVICE#GENERAL": "staff",
    "FOOD#PRICES": "price",
    "RESTAURANT#PRICES": "price",
    "DRINKS#PRICES": "price",
    "LOCATION#GENERAL": "location",
}


def clean_text(text):
    """Normalises the text without removing any letters."""
    # NFC: "č" is always stored as one character, not "c" + accent
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_aspect_labels(sentence):
    """Returns a label for each aspect: none, positive, negative, neutral or conflict."""
    polarities = {aspect: set() for aspect in ASPECTS}
    for opinion in sentence.iter("Opinion"):
        aspect = CATEGORY_MAP.get(opinion.get("category"))
        if aspect is not None:
            polarities[aspect].add(opinion.get("polarity"))

    labels = {}
    for aspect in ASPECTS:
        if len(polarities[aspect]) == 0:
            labels[aspect] = "none"         
        elif len(polarities[aspect]) == 1:
            labels[aspect] = polarities[aspect].pop()
        else:
            labels[aspect] = "conflict"     # same aspect, different polarities
    return labels


def read_semeval(file_name, language):
    """Reads one SemEval XML file and returns a table with one row per sentence."""
    root = ET.parse(os.path.join(RAW_DIR, file_name)).getroot()
    rows = []
    for review in root.iter("Review"):
        for sentence in review.iter("sentence"):
            row = {
                "review_id": review.get("rid"),
                "sentence_id": sentence.get("id"),
                "language": language,
                "domain": "restaurant",
                "text": clean_text(sentence.find("text").text),
            }
            row.update(get_aspect_labels(sentence))
            rows.append(row)
    return pd.DataFrame(rows)


def split_by_review(df, val_ratio, seed):
    """Splits into train and validation so that all sentences of one review stay together."""
    review_ids = sorted(df["review_id"].unique())
    random.Random(seed).shuffle(review_ids)
    n_val = int(len(review_ids) * val_ratio)
    val_ids = set(review_ids[:n_val])
    val_mask = df["review_id"].isin(val_ids)
    return df[~val_mask], df[val_mask]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    en_train_full = read_semeval("restaurants_train_english.xml", "en")
    en_test = read_semeval("restaurants_test_english.xml", "en")
    tr_test = pd.concat([
        read_semeval("restaurants_train_turkish.xml", "tr"),
        read_semeval("restaurants_test_turkish.xml", "tr"),
    ])

    en_train, en_val = split_by_review(en_train_full, VAL_RATIO, SEED)

    datasets = {
        "en_train": en_train,
        "en_val": en_val,
        "en_test": en_test,
        "tr_test": tr_test,
    }

    for name, df in datasets.items():
        out_path = os.path.join(OUT_DIR, f"{name}.csv")
        df.to_csv(out_path, index=False, encoding="utf-8")

        n_conflict = sum((df[aspect] == "conflict").sum() for aspect in ASPECTS)
        n_no_aspect = (df[ASPECTS] == "none").all(axis=1).sum()
        print(f"{name}: {len(df)} sentences, {df['review_id'].nunique()} reviews, "
              f"{n_no_aspect} without aspects, {n_conflict} conflict labels -> {out_path}")


if __name__ == "__main__":
    main()