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
    "affordable": "#2C2C63",
    "critical": "#7C7CC4", 
    "not_affordable": "#FE9542",
    "structurally_excluded": "#660000",
}

CITY_DISTRICT_MAPPING = {
    "zentrum": "Mitte",
    "zentrum_nord": "Mitte",
    "zentrum_nordwest": "Mitte",
    "zentrum_ost": "Mitte",
    "zentrum_sued": "Mitte",
    "zentrum_suedost": "Mitte",
    "zentrum_west": "Mitte",

    "gohlis_nord": "Nord",
    "gohlis_mitte": "Nord",
    "gohlis_sued": "Nord",
    "eutritzsch": "Nord",
    "seehausen": "Nord",
    "wiederitzsch": "Nord",

    "mockau_nord": "Nordost",
    "mockau_sued": "Nordost",
    "plaussig_portitz": "Nordost",
    "schoenefeld_abtnaundorf": "Nordost",
    "schoenefeld_ost": "Nordost",
    "thekla": "Nordost",

    "althen_kleinpoesna": "Ost",
    "anger_crottendorf": "Ost",
    "baalsdorf": "Ost",
    "engelsdorf": "Ost",
    "heiterblick": "Ost",
    "moelkau": "Ost",
    "neustadt_neuschoenefeld": "Ost",
    "paunsdorf": "Ost",
    "sellerhausen_stuenz": "Ost",
    "volkmarsdorf": "Ost",

    "holzhausen": "Suedost",
    "liebertwolkwitz": "Suedost",
    "meusdorf": "Suedost",
    "probstheida": "Suedost",
    "reudnitz_thonberg": "Suedost",
    "stoetteritz": "Suedost",

    "connewitz": "Sued",
    "doelitz_doesen": "Sued",
    "loessnig": "Sued",
    "marienbrunn": "Sued",
    "suedvorstadt": "Sued",

    "grosszschocher": "Suedwest",
    "hartmannsdorf_knautnaundorf": "Suedwest",
    "kleinzschocher": "Suedwest",
    "knautkleeberg_knauthain": "Suedwest",
    "plagwitz": "Suedwest",
    "schleussig": "Suedwest",

    "gruenau_nord": "West",
    "gruenau_mitte": "West",
    "gruenau_ost": "West",
    "gruenau_siedlung": "West",
    "lausen_gruenau": "West",
    "miltitz": "West",
    "schoenau": "West",

    "burghausen_rueckmarsdorf": "Altwest",
    "boehlitz_ehrenberg": "Altwest",
    "leutzsch": "Altwest",
    "lindenau": "Altwest",
    "neulindenau": "Altwest",
    "altlindenau": "Altwest",

    "lindenthal": "Nordwest",
    "luetzschena_stahmeln": "Nordwest",
    "moeckern": "Nordwest",
    "wahren": "Nordwest",
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

    city_outline = merged.dissolve()

    # 1. Weißer Außen-Halo zuerst, unter der Karte
    city_outline.boundary.plot(
        ax=ax,
        color="white",
        linewidth=50,
        zorder=0,
    )

    # 2. Danach normale Karte darüber
    merged.plot(
        color=merged["affordability_status"].map(COLORS).fillna("#DDDDDD"),
        edgecolor=(1, 1, 1, 0.35),
        linewidth=0.7,
        ax=ax,
        zorder=1,
    )

    merged["city_district"] = merged["district_id"].map(CITY_DISTRICT_MAPPING)

    city_district_borders = merged.dissolve(by="city_district")

    # 3. Stadtbezirksgrenzen wie bisher
    city_district_borders.boundary.plot(
        ax=ax,
        color="#FFFFFF",
        linewidth=1.86,
        zorder=10,
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
