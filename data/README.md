# Data

## English and Turkish data (SemEval-2016 Task 5)

We use the restaurant reviews from SemEval-2016 Task 5, Subtask 1 (sentence-level ABSA)
(Pontiki et al., 2016).

- Official page: https://alt.qcri.org/semeval2016/task5/
- We download a corrected copy from GitHub: https://github.com/YaxinCui/ABSADataset
- English hotel reviews are not part of SemEval-2016, so we train on restaurant reviews only.

Raw files are not included in this repository. To download them, run from the project root:

    python src/download_data.py

The files are saved to `data/raw/`.

### Dataset size

| File | Sentences | Sentences without opinions |
|---|---|---|
| English train | 2000 | 292 |
| English test | 676 | 89 |
| Turkish train | 1232 | 128 |
| Turkish test | 144 | 20 |

### How we use the data

- English train: split into training and validation sets
- English test: official English test set
- Turkish train + test: used only for testing (zero-shot); the model is never trained on Turkish

## Category mapping

SemEval uses ENTITY#ATTRIBUTE categories. We map them to our four aspects:

| Our aspect | SemEval categories | Opinions (English train) |
|---|---|---|
| food | FOOD#QUALITY, FOOD#STYLE_OPTIONS, DRINKS#QUALITY, DRINKS#STYLE_OPTIONS | 1065 |
| staff | SERVICE#GENERAL | 449 |
| price | FOOD#PRICES, RESTAURANT#PRICES, DRINKS#PRICES | 190 |
| location | LOCATION#GENERAL | 28 |
| ignored | RESTAURANT#GENERAL, RESTAURANT#MISCELLANEOUS, AMBIENCE#GENERAL | 775 |

Mapping rules:

1. Prices of food and drinks are mapped to `price`, not `food`.
2. Drinks are mapped to `food`.
3. Ambience and general restaurant opinions are not among our aspects and are ignored.
   A sentence with only these opinions becomes a sentence without aspects.
4. If one sentence has the same aspect with different polarities after mapping
   (e.g. positive starter, negative beer), the aspect is marked as present and its
   sentiment is labelled `conflict`. Conflict labels are not used to train the sentiment model.

Known challenges:

- `location` is very rare (28 opinions in 2000 English training sentences).
- `neutral` is rare (101 of 2507 English training opinions).
- The training data contains only restaurants, while our Bosnian test set also contains hotels.

## License

The official SemEval-2016 Task 5 page (Data and Tools) does not state an explicit license
for the data. The official download links point to the META-SHARE repository
(metashare.ilsp.gr), which was not reachable when we tried to access it (13.11.2026).
For this reason we download a corrected copy of the data from GitHub
(https://github.com/YaxinCui/ABSADataset).

The data was released by the task organisers for research purposes. Because the
redistribution terms are not clear, we do not include the raw files in this repository.
If you use the data, cite: Pontiki et al. (2016), SemEval-2016 Task 5: Aspect Based
Sentiment Analysis, Proceedings of SemEval-2016, pp. 19–30.
