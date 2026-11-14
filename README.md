# Cross-Lingual Aspect-Based Sentiment Analysis of Tourist Reviews of Sarajevo Restaurants and Hotels

NLP course project – Topic 6: Tourist review aspect analysis

## Team
- Merima Balihodžić – Merima667
- Medina Alić – medina1908
- Selma Melunović– SelmaMelunovic

## Topic
We detect which aspects (food, staff, price, location) tourists mention in reviews of
Sarajevo restaurants and hotels, and whether they praise or criticise them.
We test whether a model trained on English reviews works on Bosnian and other
languages without retraining.

## Status
## Research question
Does an aspect model trained on English reviews work on Bosnian and other languages
without retraining?

## Data
- Training: SemEval-2016 Task 5, English restaurant reviews
- Testing: SemEval-2016 English and Turkish restaurant reviews, and our own annotated
  Bosnian reviews of Sarajevo restaurants and hotels

Details about the data, the license and the category mapping: see [`data/README.md`](data/README.md).

## Installation
Requires Python 3.12.

    pip install -r requirements.txt

## How to run
Run all commands from the project root, in this order:

    python src/download_data.py      # downloads SemEval-2016 data to data/raw/
    python src/preprocess.py         # cleans, maps categories, splits data -> data/processed/
    python src/analyze_data.py       # tables and charts -> results/data_analysis/

The random seed is fixed (`SEED = 42` in `src/preprocess.py`), so the split is always the same.

## Repository structure

    data/          data instructions; raw/ and processed/ are not in the repository
    src/           Python scripts
    results/       tables, charts and model results
    docs/          AI log, annotation guidelines, pipeline diagram
    notebooks/     experiments

## Pipeline

```mermaid
flowchart LR
    subgraph DATA["Data"]
        A1["SemEval-2016 Task 5<br/>English + Turkish<br/>(external)"]:::ext
        A2["Bosnian reviews<br/>Sarajevo restaurants + hotels<br/>(own collection)"]:::own
    end

    subgraph PREP["Preprocessing"]
        B1["download_data.py<br/>preprocess.py<br/>category mapping<br/>(own)"]:::own
        B2["Anonymisation<br/>sentence splitting<br/>manual annotation<br/>(own)"]:::own
    end

    A1 --> B1
    A2 --> B2

    B1 --> C1["en_train / en_val / en_test<br/>tr_test"]:::own
    B2 --> C2["bs_test<br/>(own test set)"]:::own

    C1 --> D0["Data analysis<br/>analyze_data.py<br/>(own)"]:::own
    C2 --> D0

    subgraph MODELS["Methods"]
        D1["Baseline<br/>(own)"]:::own
        D2["XLM-R pretrained model<br/>(external)"]:::ext
        D3["Fine-tuning on English<br/>(own)"]:::own
        D4["Translate-test:<br/>machine translation to English<br/>(external)"]:::ext
    end

    C1 --> D1
    C1 --> D3
    D2 --> D3
    C2 --> D4
    D4 --> D3

    D1 --> E["Evaluation<br/>F1 per aspect, per language,<br/>restaurant vs hotel<br/>(own)"]:::own
    D3 --> E
    C2 --> E

    classDef own fill:#d4edda,stroke:#2e7d32,color:#000
    classDef ext fill:#e3e8f0,stroke:#546e7a,color:#000
```

Green: our own work. Grey: external data, models or services.

## Status
Milestone 3: data, preprocessing and data analysis done; baseline and Bosnian test set in progress.
