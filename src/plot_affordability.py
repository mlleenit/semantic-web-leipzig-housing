from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_FILE = "data_processed/affordability_observations.csv"
OUTPUT_DIR = Path("visual_output")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(INPUT_FILE)

    # Plot 1: affordability status counts by income scenario
    status_counts = (
        df.groupby(["income_scenario_id", "affordability_status"])
        .size()
        .unstack(fill_value=0)
    )

    ax = status_counts.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Affordability status counts by income scenario")
    ax.set_xlabel("Income scenario")
    ax.set_ylabel("Number of Leipzig districts")
    ax.legend(title="Affordability status")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "affordability_status_by_income_scenario.png", dpi=300)
    plt.close()

    # Plot 2: direct comparison of housing stress scores by district
    comparison = df.pivot(
        index="district_id",
        columns="income_scenario_id",
        values="housing_stress_score",
    )

    comparison = comparison.sort_values("bafog_only", ascending=False)

    ax = comparison.plot(kind="bar", figsize=(18, 7))
    ax.axhline(0.30, linestyle="--", label="affordable threshold")
    ax.axhline(0.45, linestyle="--", label="critical threshold")
    ax.axhline(0.60, linestyle="--", label="structural exclusion threshold")
    ax.set_title("Housing stress score by district and income scenario")
    ax.set_xlabel("District")
    ax.set_ylabel("Warm rent / monthly income")
    ax.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "housing_stress_by_district_and_scenario.png", dpi=300)
    plt.close()

    # Plot 3: top 15 highest BAföG-only stress districts with Minijob comparison
    top15_districts = (
        df[df["income_scenario_id"] == "bafog_only"]
        .sort_values("housing_stress_score", ascending=False)
        .head(15)["district_id"]
    )

    top15_comparison = comparison.loc[top15_districts]

    ax = top15_comparison.plot(kind="bar", figsize=(14, 6))
    ax.axhline(0.30, linestyle="--", label="affordable threshold")
    ax.axhline(0.45, linestyle="--", label="critical threshold")
    ax.axhline(0.60, linestyle="--", label="structural exclusion threshold")
    ax.set_title("Top 15 highest student housing stress districts: BAföG vs Minijob")
    ax.set_xlabel("District")
    ax.set_ylabel("Warm rent / monthly income")
    ax.legend()
    plt.xticks(rotation=75, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top15_bafog_vs_minijob.png", dpi=300)
    plt.close()

    print("Saved plots:")
    print(OUTPUT_DIR / "affordability_status_by_income_scenario.png")
    print(OUTPUT_DIR / "housing_stress_by_district_and_scenario.png")
    print(OUTPUT_DIR / "top15_bafog_vs_minijob.png")


if __name__ == "__main__":
    main()