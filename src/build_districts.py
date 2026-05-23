from pathlib import Path

import geopandas as gpd
import pandas as pd


INPUT_FILE = Path("data_raw/geo/Ortsteile_Leipzig_UTM33N.json")
OUTPUT_FILE = Path("data_processed/districts.csv")


def normalize_district_id(name: str) -> str:
    name = name.strip().lower()

    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
    }

    for old, new in replacements.items():
        name = name.replace(old, new)

    name = name.replace("-", "_")
    name = name.replace(" ", "_")

    return name


def main() -> None:
    gdf = gpd.read_file(INPUT_FILE)

    # Try to detect the district name column automatically
    possible_columns = [
        "name",
        "Name",
        "ORTSTEIL",
        "ortsteil",
        "stadtteil",
        "Stadtteil",
    ]

    district_column = None

    for column in possible_columns:
        if column in gdf.columns:
            district_column = column
            break

    if district_column is None:
        raise ValueError(
            f"Could not find district name column. Available columns: {list(gdf.columns)}"
        )

    result = pd.DataFrame()

    result["district_name"] = gdf[district_column]
    result["district_id"] = result["district_name"].apply(normalize_district_id)

    result["city"] = "Leipzig"
    result["country"] = "Germany"

    # Optional Linked Data fields
    result["linked_geo_uri"] = ""
    result["dbpedia_uri"] = ""

    result = result[
        [
            "district_id",
            "district_name",
            "city",
            "country",
            "linked_geo_uri",
            "dbpedia_uri",
        ]
    ]

    result = result.sort_values("district_id")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print(result.head())
    print("Rows written:", len(result))
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()