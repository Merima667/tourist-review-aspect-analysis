"""
Downloads SemEval-2016 Task 5 restaurant data (English and Turkish) into data/raw/.
Source: corrected copy of the original data on GitHub (YaxinCui/ABSADataset).
Original: https://alt.qcri.org/semeval2016/task5/
"""
import os
import urllib.request

BASE_URL = "https://raw.githubusercontent.com/YaxinCui/ABSADataset/main/SemEval2016Task5Corrected"
OUT_DIR = os.path.join("data", "raw")

FILES = [
    ("train", "english"),
    ("test", "english"),
    ("train", "turkish"),
    ("test", "turkish"),
]
os.makedirs(OUT_DIR, exist_ok=True)

for split, lang in FILES:
    name = f"restaurants_{split}_{lang}.xml"
    url = f"{BASE_URL}/{split}/{name}"
    out_path = os.path.join(OUT_DIR, name)
    print("Downloading", name, "...")
    urllib.request.urlretrieve(url, out_path)

print("Done. Files saved to", OUT_DIR)