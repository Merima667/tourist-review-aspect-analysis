"""
Counts sentences, opinions, categories and polarities in the SemEval-2016 files.
Used to decide how to map SemEval categories to our four aspects.
"""
import os
import xml.etree.ElementTree as ET
from collections import Counter

RAW_DIR = os.path.join("data", "raw")
FILES = [
    "restaurants_train_english.xml",
    "restaurants_test_english.xml",
    "restaurants_train_turkish.xml",
    "restaurants_test_turkish.xml",
]

for file_name in FILES:
    root = ET.parse(os.path.join(RAW_DIR, file_name)).getroot()

    n_sentences = 0
    n_without_opinions = 0
    categories = Counter()
    polarities = Counter()

    for sentence in root.iter("sentence"):
        n_sentences += 1
        opinions = list(sentence.iter("Opinion"))
        if len(opinions) == 0:
            n_without_opinions += 1
        for opinion in opinions:
            categories[opinion.get("category")] += 1
            polarities[opinion.get("polarity")] += 1

    print("=" * 50)
    print(file_name)
    print("Sentences:", n_sentences)
    print("Sentences without opinions:", n_without_opinions)
    print("Polarities:", dict(polarities))
    print("Categories:")
    for category, count in categories.most_common():
        print(f"  {category:30} {count}")