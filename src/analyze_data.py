"""
Data analysis for the processed datasets.

Creates two tables and two charts and saves them to results/data_analysis/:
- Table 1: size of each dataset
- Table 2: label counts per aspect in each dataset
- Chart 1: how often each aspect is mentioned, per dataset
- Chart 2: sentiment distribution per aspect in the English training data

Run src/preprocess.py first.
"""
import os

import matplotlib.pyplot as plt
import pandas as pd

PROCESSED_DIR = os.path.join("data", "processed")
OUT_DIR = os.path.join("results", "data_analysis")

ASPECTS = ["food", "staff", "price", "location"]
LABELS = ["positive", "negative", "neutral", "conflict"]
DATASETS = ["en_train", "en_val", "en_test", "tr_test"]

# Colours for the charts (colour-blind friendly)
DATASET_COLORS = {"en_train": "#2a78d6", "en_test": "#eb6834", "tr_test": "#1baf7a"}
LABEL_COLORS = {"positive": "#2a78d6", "negative": "#eb6834",
                "neutral": "#a3a29c", "conflict": "#6250d6"}


def load_datasets():
    """Loads all processed CSV files into a dictionary {name: table}."""
    return {name: pd.read_csv(os.path.join(PROCESSED_DIR, f"{name}.csv"), encoding="utf-8")
            for name in DATASETS}


def table_dataset_sizes(data):
    """Table 1: number of reviews and sentences, and sentences without any aspect."""
    rows = []
    for name, df in data.items():
        no_aspect = (df[ASPECTS] == "none").all(axis=1).sum()
        rows.append({
            "dataset": name,
            "reviews": df["review_id"].nunique(),
            "sentences": len(df),
            "sentences_without_aspect": no_aspect,
            "percent_without_aspect": round(100 * no_aspect / len(df), 1),
        })
    return pd.DataFrame(rows)


def table_label_counts(data):
    """Table 2: how many sentences have each label, for each aspect and dataset."""
    rows = []
    for name, df in data.items():
        for aspect in ASPECTS:
            counts = df[aspect].value_counts()
            row = {"dataset": name, "aspect": aspect}
            for label in LABELS:
                row[label] = int(counts.get(label, 0))
            row["total_mentioned"] = sum(row[label] for label in LABELS)
            rows.append(row)
    return pd.DataFrame(rows)


def chart_aspect_frequency(data, out_path):
    """Chart 1: percentage of sentences that mention each aspect, per dataset."""
    names = ["en_train", "en_test", "tr_test"]
    bar_width = 0.25
    fig, ax = plt.subplots(figsize=(8, 4.5))

    for i, name in enumerate(names):
        df = data[name]
        percents = [100 * (df[aspect] != "none").mean() for aspect in ASPECTS]
        positions = [x + (i - 1) * bar_width for x in range(len(ASPECTS))]
        bars = ax.bar(positions, percents, width=bar_width - 0.03,
                      color=DATASET_COLORS[name], label=name)
        ax.bar_label(bars, fmt="%.1f", fontsize=8, padding=2)

    ax.set_xticks(range(len(ASPECTS)))
    ax.set_xticklabels(ASPECTS)
    ax.set_ylabel("% of sentences mentioning the aspect")
    ax.set_title("How often each aspect is mentioned")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def chart_sentiment_per_aspect(df, out_path):
    """Chart 2: share of each sentiment label per aspect (English training data)."""
    fig, ax = plt.subplots(figsize=(8, 4))
    y_labels = []

    for y, aspect in enumerate(ASPECTS):
        mentioned = df[df[aspect] != "none"][aspect]
        total = len(mentioned)
        y_labels.append(f"{aspect} (n={total})")
        left = 0
        for label in LABELS:
            share = 100 * (mentioned == label).sum() / total
            ax.barh(y, share, left=left, color=LABEL_COLORS[label],
                    edgecolor="white", linewidth=1.5,
                    label=label if y == 0 else None)
            if share >= 6:
                ax.text(left + share / 2, y, f"{share:.0f}%", ha="center",
                        va="center", color="white", fontsize=8)
            left += share

    ax.set_yticks(range(len(ASPECTS)))
    ax.set_yticklabels(y_labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of sentences that mention the aspect")
    ax.set_title("Sentiment per aspect (English training data)")
    ax.legend(ncol=4, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    data = load_datasets()

    sizes = table_dataset_sizes(data)
    sizes.to_csv(os.path.join(OUT_DIR, "table1_dataset_sizes.csv"), index=False)
    print("Table 1: dataset sizes")
    print(sizes.to_string(index=False), "\n")

    labels = table_label_counts(data)
    labels.to_csv(os.path.join(OUT_DIR, "table2_label_counts.csv"), index=False)
    print("Table 2: label counts per aspect")
    print(labels.to_string(index=False), "\n")

    chart_aspect_frequency(data, os.path.join(OUT_DIR, "chart1_aspect_frequency.png"))
    chart_sentiment_per_aspect(data["en_train"],
                               os.path.join(OUT_DIR, "chart2_sentiment_per_aspect.png"))
    print("Charts saved to", OUT_DIR)


if __name__ == "__main__":
    main()