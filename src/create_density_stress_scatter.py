from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]

AFFORDABILITY_PATH = (
    BASE_DIR / "data_processed" / "affordability_observations.csv"
)

DENSITY_PATH = (
    BASE_DIR
    / "data_raw"
    / "population"
    / "Bevölkerungsbestand_Einwohnerdichte_Ortsteile.csv"
)

OUTPUT_DIR = BASE_DIR / "visual_output"

OUTPUT_DIR.mkdir(exist_ok=True)


def normalize_district_name(name: str) -> str:
    name = str(name).lower().strip()

    name = name.replace("ä", "ae")
    name = name.replace("ö", "oe")
    name = name.replace("ü", "ue")
    name = name.replace("ß", "ss")

    name = name.replace("-", "_")
    name = name.replace(" ", "_")

    return name


def main() -> None:

    affordability = pd.read_csv(AFFORDABILITY_PATH)

    affordability = affordability[
        affordability["income_scenario_id"] == "bafog_only"
    ].copy()

    density = pd.read_csv(DENSITY_PATH)

    density["district_id"] = density["Gebiet"].apply(
        normalize_district_name
    )

    merged = affordability.merge(
        density[["district_id", "2025"]],
        on="district_id",
        how="inner",
    )

    merged["2025"] = (
        merged["2025"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    fig, ax = plt.subplots(figsize=(10, 8))

    scatter = ax.scatter(
        merged["2025"],
        merged["housing_stress_score"],
        s=120,
        alpha=0.8,
        color="#7C7CC4",
        edgecolors="#2C2C63",
        linewidths=0.7,
    )

    important = [
        "zentrum_ost",
        "zentrum_nord",
        "zentrum_sued",
        "neustadt_neuschoenefeld",
        "gohlis_mitte",
    ]

    for _, row in merged.iterrows():

        if row["district_id"] in important:

            ax.annotate(
                row["district_id"]
                .replace("_", " ")
                .title(),
                (
                    row["2025"],
                    row["housing_stress_score"],
                ),
                fontsize=8,
            )

    ax.set_xlabel(
        "Population density (inhabitants/km²)",
        fontsize=12,
    )

    ax.set_ylabel(
        "Housing stress score",
        fontsize=12,
    )

    ax.set_title(
        "Population density vs housing stress",
        fontsize=14,
        weight="bold",
    )

    ax.grid(
        alpha=0.2,
        linestyle="--",
    )

    plt.tight_layout()

    output_file = (
        OUTPUT_DIR
        / "population_density_vs_housing_stress.png"
    )

    plt.savefig(
        output_file,
        dpi=600,
        bbox_inches="tight",
        transparent=True,
    )

    plt.close()

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()