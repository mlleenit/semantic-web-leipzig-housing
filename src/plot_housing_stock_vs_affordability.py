from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


AFFORDABILITY_FILE = "data_processed/affordability_observations.csv"
HOUSING_STOCK_FILE = "data_processed/housing_stock_observations.csv"
OUTPUT_FILE = "visual_output/housing_stock_vs_affordability.png"


def main() -> None:
    affordability = pd.read_csv(AFFORDABILITY_FILE)
    housing_stock = pd.read_csv(HOUSING_STOCK_FILE)

    affordability_bafog = affordability[
        affordability["income_scenario_id"] == "bafog_only"
    ][
        ["district_id", "housing_stress_score", "affordability_status"]
    ]

    housing_2024 = housing_stock[housing_stock["year"] == 2024][
        ["district_id", "district_name", "housing_units"]
    ]

    merged = housing_2024.merge(
        affordability_bafog,
        on="district_id",
        how="inner",
    )

    plot_data = merged.sort_values("housing_units", ascending=False).head(15)

    Path("visual_output").mkdir(exist_ok=True)

    ax = plot_data.plot(
        x="district_name",
        y="housing_units",
        kind="bar",
        figsize=(12, 6),
        legend=False,
    )

    ax.set_title("Top Leipzig districts by housing stock and student housing stress")
    ax.set_xlabel("District")
    ax.set_ylabel("Housing units in 2024")

    ax2 = ax.twinx()
    ax2.plot(
        ax.get_xticks(),
        plot_data["housing_stress_score"],
        marker="o",
        linestyle="-",
    )
    ax2.set_ylabel("Housing stress score (BAföG only)")

    ax2.axhline(0.30, linestyle="--")
    ax2.axhline(0.45, linestyle="--")
    ax2.axhline(0.60, linestyle="--")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(OUTPUT_FILE, dpi=300)
    plt.close()

    print(f"Saved plot to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()