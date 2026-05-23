from pathlib import Path
import re

import pandas as pd
import pdfplumber


INPUT_FILE = Path("data_raw/rents/Mietspiegel_Leipzig_2026.pdf")
OUTPUT_FILE = Path("data_processed/rent_observations.csv")

YEAR = 2026
FLAT_SIZE_SQM = 30
UTILITIES_EUR = 120
SOURCE_ID = "wohnungsboerse_2026"


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

    manual_mappings = {
        "knauthain_knautkleeberg": "knautkleeberg_knauthain",
    }

    return manual_mappings.get(name, name)


def parse_rent_value(value: str) -> float:
    value = value.replace("€", "").replace(",", ".").strip()
    return float(value)


def extract_district_rents_from_pdf(pdf_path: Path) -> pd.DataFrame:
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        # Stadtteil-Miettabelle steht in der PDF auf Seite 3 und 4.
        # pdfplumber zählt ab 0, deshalb: [2, 3]
        for page_index in [2, 3]:
            page = pdf.pages[page_index]
            tables = page.extract_tables()

            for table in tables:
                for row in table:
                    if not row:
                        continue

                    cells = [cell.strip() if cell else "" for cell in row]

                    if len(cells) < 5:
                        continue

                    # Tabellenstruktur:
                    # Stadtteil | €/m² | leer | Stadtteil | €/m²
                    pairs = [
                        (cells[0], cells[1]),
                        (cells[3], cells[4]),
                    ]

                    for district_name, rent_value in pairs:
                        if not district_name or not rent_value:
                            continue

                        if "Stadtteil" in district_name or "€" in district_name:
                            continue

                        if district_name.strip().isdigit():
                            continue

                        if not re.search(r"\d+,\d+", rent_value):
                            continue

                        rows.append(
                            {
                                "district_name": district_name,
                                "offer_rent_per_sqm": parse_rent_value(rent_value),
                            }
                        )

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("No rent observations could be extracted from the PDF.")

    df["district_id"] = df["district_name"].apply(normalize_district_id)
    df = df.drop_duplicates(subset=["district_id"])
    df = df.sort_values("district_id")

    return df


def main() -> None:
    rents = extract_district_rents_from_pdf(INPUT_FILE)

    records = []

    for _, row in rents.iterrows():
        district_id = row["district_id"]

        records.append(
            {
                "observation_id": f"rent_{district_id}_{YEAR}",
                "district_id": district_id,
                "year": YEAR,
                "offer_rent_per_sqm": row["offer_rent_per_sqm"],
                "flat_size_sqm": FLAT_SIZE_SQM,
                "utilities_eur": UTILITIES_EUR,
                "source_id": SOURCE_ID,
                "notes": "Offer rent per sqm automatically extracted from Wohnungsboerse Leipzig PDF",
            }
        )

    result = pd.DataFrame(records)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print(result.head())
    print("Rows written:", len(result))
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()