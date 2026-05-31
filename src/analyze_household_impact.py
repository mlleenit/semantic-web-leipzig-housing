from pathlib import Path

import pandas as pd
import unicodedata


BASE_DIR = Path(__file__).resolve().parents[1]

AFFORDABILITY_PATH = BASE_DIR / "data_processed" / "affordability_observations.csv"
HOUSEHOLDS_PATH = BASE_DIR / "data_raw" / "population" / "Bevölkerungsbestand_Personenhaushalte.csv"


def normalize_name(name: str) -> str:
    name = str(name).lower()

    name = name.replace("ä", "ae")
    name = name.replace("ö", "oe")
    name = name.replace("ü", "ue")
    name = name.replace("ß", "ss")

    name = "".join(
        c for c in name
        if c.isalnum()
    )

    return name


def main():
    affordability = pd.read_csv(AFFORDABILITY_PATH)

    affordability = affordability[
        affordability["income_scenario_id"] == "bafog_only"
    ]

    households = pd.read_csv(HOUSEHOLDS_PATH)

    households = households[
        households["Sachmerkmal"] == "Haushalte insgesamt"
    ].copy()

    households["district_name"] = households["Gebiet"]
    households["households_2025"] = households["2025"]

    households["households_2025"] = (
    households["households_2025"]
    .astype(str)
    .str.replace("\u202f", "", regex=False)  # schmales Leerzeichen
    .str.replace(" ", "", regex=False)
    .str.replace(",", ".", regex=False)
    )

    households["households_2025"] = pd.to_numeric(
        households["households_2025"],
        errors="coerce"
    )

    households["district_key"] = (
        households["district_name"]
        .apply(normalize_name)
    )

    affordability["district_key"] = (
        affordability["district_id"]
        .apply(normalize_name)
    )

    merged = affordability.merge(
        households[
            ["district_name", "district_key", "households_2025"]
        ],
        on="district_key",
        how="left"
    )

    total_households = merged["households_2025"].sum()

    not_affordable = merged[
        merged["affordability_status"] == "not_affordable"
    ]

    affected_households = (
        not_affordable["households_2025"]
        .sum()
    )

    share = (
        affected_households
        / total_households
        * 100
    )

    print("\n===== HOUSEHOLD IMPACT =====")
    print(f"Total households: {total_households:,.0f}")
    print(f"Affected households: {affected_households:,.0f}")
    print(f"Share: {share:.1f}%")

    print("\nAffected districts:")
    print(
        not_affordable[
            ["district_name", "households_2025"]
        ]
        .sort_values(
            "households_2025",
            ascending=False
        )
    )
    print(merged["households_2025"].head())
    print(merged["households_2025"].dtype)

    unmatched = merged[merged["households_2025"].isna()]

    print("\nUnmatched districts:")
    print(unmatched[["district_id"]])
    print(f"\nNumber of unmatched districts: {len(unmatched)}")


if __name__ == "__main__":
    main()