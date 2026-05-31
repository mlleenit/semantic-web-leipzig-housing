from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]

AFFORDABILITY_PATH = BASE_DIR / "data_processed" / "affordability_observations.csv"
OUTPUT_DIR = BASE_DIR / "visual_output"
OUTPUT_PATH = OUTPUT_DIR / "donut_bafög_minijob.png"

OUTPUT_DIR.mkdir(exist_ok=True)


STATUS_LABELS = {
    "affordable": "Leistbar",
    "critical": "Kritisch",
    "not_affordable": "Nicht leistbar",
    "structurally_excluded": "Strukturell\nausgeschlossen",
}

STATUS_COLORS = {
    "affordable": "#2C2C63", 
    "critical": "#7C7CC4",
    "not_affordable": "#FE9542",
    "structurally_excluded": "#F0F6E2",
}


def main():
    df = pd.read_csv(AFFORDABILITY_PATH)

    print("Income scenarios:")
    print(df["income_scenario_id"].unique())

    scenario = "bafog_plus_minijob"

    df = df[df["income_scenario_id"] == scenario]

    print(f"Rows after filter: {len(df)}")

    counts = (
        df["affordability_status"]
        .value_counts()
        .reindex(STATUS_LABELS.keys(), fill_value=0)
    )

    percentages = counts / counts.sum() * 100

    labels = [
        f"{STATUS_LABELS[status]}\n{percentages[status]:.0f}%"
        for status in counts.index
        if counts[status] > 0
    ]

    values = [counts[status] for status in counts.index if counts[status] > 0]
    colors = [STATUS_COLORS[status] for status in counts.index if counts[status] > 0]

    fig, ax = plt.subplots(figsize=(6, 6), facecolor="white")
    ax.set_facecolor("white")

    ax.pie(
        values,
        labels=labels,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.42, "edgecolor": "white", "linewidth": 2},
        labeldistance=1.12,
        textprops={"fontsize": 11},
    )

    ax.set_title("BAföG + Minijob", fontsize=16, fontweight="bold", pad=18)
    ax.set_aspect("equal")

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300, facecolor="white", bbox_inches="tight")
    plt.close()

    print(f"Saved donut chart to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()