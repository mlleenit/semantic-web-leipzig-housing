from pathlib import Path
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


BASE_DIR = Path(__file__).resolve().parents[1]

GEO_PATH = BASE_DIR / "data_raw" / "geo" / "Ortsteile_Leipzig_UTM33N.json"
AFFORDABILITY_PATH = BASE_DIR / "data_processed" / "affordability_observations.csv"
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


def classify_affordability(score: float) -> str:
    if score <= 0.30:
        return "affordable"
    if score <= 0.45:
        return "critical"
    if score <= 0.60:
        return "not_affordable"
    return "structurally_excluded"


COLORS = {
    "affordable": "#7C7CC4",
    "critical": "#7C7CC4", 
    "not_affordable": "#FE9542",
    "structurally_excluded": "#2C2C63",
}

LABELS = {
    "affordable": "Leistbar",
    "critical": "Kritisch",
    "not_affordable": "Nicht leistbar",
    "structurally_excluded": "Strukturell ausgeschlossen",
}


def create_bafog_only_map() -> None:
    districts = gpd.read_file(GEO_PATH)
    affordability = pd.read_csv(AFFORDABILITY_PATH)

    districts["district_id"] = districts["Name"].apply(normalize_district_name)

    bafog_data = affordability[
        affordability["income_scenario_id"] == "bafog_only"
    ].copy()

    bafog_data["affordability_status"] = bafog_data[
        "housing_stress_score"
    ].apply(classify_affordability)

    merged = districts.merge(bafog_data, on="district_id", how="left")

    print("\n=== DEBUGGING DISTRICT IDS ===")

    geo_ids = set(districts["district_id"])
    aff_ids = set(bafog_data["district_id"])

    print("\nIn Geo-Datei, aber nicht in Affordability:")
    print(sorted(geo_ids - aff_ids))

    print("\nIn Affordability, aber nicht in Geo-Datei:")
    print(sorted(aff_ids - geo_ids))

    print("\nAnzahl Geo IDs:", len(geo_ids))
    print("Anzahl Affordability IDs:", len(aff_ids))

    missing = merged[merged["affordability_status"].isna()]["Name"].tolist()
    if missing:
        print("Missing affordability data:")
        print(missing)

    fig, ax = plt.subplots(figsize=(10, 12))

    merged.plot(
        color=merged["affordability_status"].map(COLORS).fillna("#DDDDDD"),
        edgecolor="white",
        linewidth=0.6,
        ax=ax,
    )

    ax.axis("off")

    output_path = OUTPUT_DIR / "map_affordability_bafog_only.png"

    plt.savefig(output_path, dpi=600, bbox_inches="tight", transparent=True)
    plt.close()

    print(f"Saved: {output_path}")


def main() -> None:
    create_bafog_only_map()


if __name__ == "__main__":
    main()