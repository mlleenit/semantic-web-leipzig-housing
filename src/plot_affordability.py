from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_FILE = "data_processed/affordability_observations.csv"
OUTPUT_DIR = Path("visual_output")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(INPUT_FILE)

    # Plot 1: status counts by social group
    status_counts = (
        df.groupby(["group_id", "affordability_status"])
        .size()
        .unstack(fill_value=0)
    )

    ax = status_counts.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Affordability status counts by social group")
    ax.set_xlabel("Social group")
    ax.set_ylabel("Number of Leipzig districts")
    ax.legend(title="Affordability status")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "affordability_status_by_group.png", dpi=300)
    plt.close()

    # Plot 2: housing stress for students by district
    students = df[df["group_id"] == "students"].sort_values(
        "housing_stress_score", ascending=False
    )

    ax = students.plot(
        kind="bar",
        x="district_id",
        y="housing_stress_score",
        figsize=(16, 6),
        legend=False,
    )
    ax.axhline(0.30, linestyle="--", label="affordable threshold")
    ax.axhline(0.45, linestyle="--", label="critical threshold")
    ax.axhline(0.60, linestyle="--", label="structural exclusion threshold")
    ax.set_title("Housing stress score for students by Leipzig district")
    ax.set_xlabel("District")
    ax.set_ylabel("Warm rent / monthly income")
    ax.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "students_housing_stress_by_district.png", dpi=300)
    plt.close()

    # Plot 3: top 15 highest housing stress observations
    top15 = df.sort_values("housing_stress_score", ascending=False).head(15)
    top15 = top15.copy()
    top15["label"] = top15["district_id"] + " / " + top15["group_id"]

    ax = top15.plot(
        kind="bar",
        x="label",
        y="housing_stress_score",
        figsize=(14, 6),
        legend=False,
    )
    ax.axhline(0.60, linestyle="--", label="structural exclusion threshold")
    ax.set_title("Top 15 highest housing stress observations")
    ax.set_xlabel("District / social group")
    ax.set_ylabel("Warm rent / monthly income")
    ax.legend()
    plt.xticks(rotation=75, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top15_housing_stress.png", dpi=300)
    plt.close()

    print("Saved plots:")
    print(OUTPUT_DIR / "affordability_status_by_group.png")
    print(OUTPUT_DIR / "students_housing_stress_by_district.png")
    print(OUTPUT_DIR / "top15_housing_stress.png")


if __name__ == "__main__":
    main()