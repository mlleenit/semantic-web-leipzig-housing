from pathlib import Path
import unicodedata

import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]

AFFORDABILITY_PATH = BASE_DIR / "data_processed" / "affordability_observations.csv"
DISTRICTS_PATH = BASE_DIR / "data_processed" / "districts.csv"

DENSITY_RAW_PATH = BASE_DIR / "data_raw" / "population" / "Bevölkerungsbestand_Einwohnerdichte_Ortsteile.csv"
HOUSEHOLDS_RAW_PATH = BASE_DIR / "data_raw" / "population" / "Bevölkerungsbestand_Personenhaushalte.csv"

OUTPUT_DIR = BASE_DIR / "visual_output"
OUTPUT_DIR.mkdir(exist_ok=True)


def normalize_name(name: str) -> str:
    name = str(name).lower().strip()
    name = name.replace("ß", "ss")
    name = unicodedata.normalize("NFKD", name)
    return "".join(c for c in name if not unicodedata.combining(c))


def read_population_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep=",", encoding="utf-8-sig")


def parse_number(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .replace("", pd.NA)
    )

    return pd.to_numeric(cleaned, errors="coerce")


def load_data() -> pd.DataFrame:
    affordability = pd.read_csv(AFFORDABILITY_PATH)
    districts = pd.read_csv(DISTRICTS_PATH)

    density_raw = read_population_csv(DENSITY_RAW_PATH)
    households_raw = read_population_csv(HOUSEHOLDS_RAW_PATH)

    districts["name_key"] = districts["district_name"].apply(normalize_name)

    density = density_raw[
        density_raw["Sachmerkmal"].eq("Einwohnerdichte")
    ][["Gebiet", "2025"]].copy()

    density.columns = ["district_name", "population_density"]
    density["name_key"] = density["district_name"].apply(normalize_name)
    density["population_density"] = parse_number(density["population_density"])
    density = density.dropna(subset=["population_density"])

    households = households_raw[
        households_raw["Sachmerkmal"].eq("Haushalte insgesamt")
    ][["Gebiet", "2025"]].copy()

    households.columns = ["district_name", "households"]
    households["name_key"] = households["district_name"].apply(normalize_name)
    households["households"] = parse_number(households["households"])
    households = households.dropna(subset=["households"])

    density = density.merge(
        districts[["district_id", "name_key"]],
        on="name_key",
        how="inner",
        validate="one_to_one",
    )

    households = households.merge(
        districts[["district_id", "name_key"]],
        on="name_key",
        how="inner",
        validate="one_to_one",
    )

    bafog = affordability[
        affordability["income_scenario_id"].eq("bafog_only")
    ][["district_id", "housing_stress_score"]].copy()

    df = (
        bafog
        .merge(
            density[["district_id", "population_density"]],
            on="district_id",
            how="inner",
            validate="one_to_one",
        )
        .merge(
            households[["district_id", "households"]],
            on="district_id",
            how="inner",
            validate="one_to_one",
        )
    )

    print()
    print("District rows:", len(districts))
    print("Density rows:", len(density))
    print("Household rows:", len(households))
    print("BAföG rows:", len(bafog))
    print("Final rows:", len(df))
    print()

    print(df.head())

    return df


def calculate_correlations(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "relationship": [
                "population_density vs housing_stress_score",
                "households vs housing_stress_score",
            ],
            "pearson_r": [
                df["population_density"].corr(
                    df["housing_stress_score"],
                    method="pearson",
                ),
                df["households"].corr(
                    df["housing_stress_score"],
                    method="pearson",
                ),
            ],
            "spearman_r": [
                df["population_density"].corr(
                    df["housing_stress_score"],
                    method="spearman",
                ),
                df["households"].corr(
                    df["housing_stress_score"],
                    method="spearman",
                ),
            ],
        }
    )


def plot_scatter(df: pd.DataFrame, x_col: str, x_label: str, filename: str) -> None:
    plt.figure(figsize=(7, 5))
    plt.scatter(df[x_col], df["housing_stress_score"], alpha=0.75)

    plt.xlabel(x_label)
    plt.ylabel("Housing Stress Score")
    plt.title(f"{x_label} vs. Housing Stress Score")
    plt.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=300)
    plt.close()


def main() -> None:
    df = load_data()

    print(f"Matched districts: {len(df)}")

    results = calculate_correlations(df)

    print("\nCorrelation results:")
    print(results.to_string(index=False))

    results.to_csv(
        OUTPUT_DIR / "correlation_results_bafog_only.csv",
        index=False,
    )

    plot_scatter(
        df,
        "population_density",
        "Population density",
        "scatter_density_stress_bafog_only.png",
    )

    plot_scatter(
        df,
        "households",
        "Number of households",
        "scatter_households_stress_bafog_only.png",
    )

    print("\nWritten files:")
    print(OUTPUT_DIR / "correlation_results_bafog_only.csv")
    print(OUTPUT_DIR / "scatter_density_stress_bafog_only.png")
    print(OUTPUT_DIR / "scatter_households_stress_bafog_only.png")


if __name__ == "__main__":
    main()