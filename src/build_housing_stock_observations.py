import pandas as pd
from pathlib import Path


INPUT_FILE = "data_raw/housing_stock/Bautätigkeit und Wohnen_Wohnungsbestand.csv"
OUTPUT_FILE = "data_processed/housing_stock_observations.csv"

YEARS = ["2020", "2021", "2022", "2023", "2024"]
SOURCE_ID = "leipzig_housing_stock"


def normalize_district_id(name: str) -> str:
    name = name.lower()

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


def main():
    df = pd.read_csv(INPUT_FILE)

    df = df[df["Sachmerkmal"] == "Wohnungen"]

    EXCLUDED_AREAS = {
    "Stadt Leipzig",
    "Mitte",
    "Nord",
    "Nordost",
    "Ost",
    "Südost",
    "Süd",
    "Südwest",
    "West",
    "Alt-West",
    "Nordwest",
    }

    df = df[~df["Gebiet"].isin(EXCLUDED_AREAS)]

    df = df[["Gebiet"] + YEARS]

    df_long = df.melt(
        id_vars=["Gebiet"],
        value_vars=YEARS,
        var_name="year",
        value_name="housing_units",
    )

    df_long["district_name"] = df_long["Gebiet"]
    df_long["district_id"] = df_long["district_name"].apply(normalize_district_id)

    df_long["year"] = df_long["year"].astype(int)
    df_long["housing_units"] = df_long["housing_units"].astype(str)
    df_long["housing_units"] = df_long["housing_units"].str.replace(",", ".", regex=False)
    df_long["housing_units"] = df_long["housing_units"].astype(float).round().astype(int)

    df_long["source_id"] = SOURCE_ID

    result = df_long[
        [
            "district_id",
            "district_name",
            "year",
            "housing_units",
            "source_id",
        ]
    ]

    Path("data_processed").mkdir(exist_ok=True)

    result.to_csv(OUTPUT_FILE, index=False)

    print(f"Wrote {len(result)} housing stock observations to {OUTPUT_FILE}")
    print(result.head())


if __name__ == "__main__":
    main()