from pathlib import Path
import re

import pandas as pd
import pdfplumber


INPUT_FILE = Path("data_raw/population/rbv-landkreisinfo_kreisfreie-stadt_leipzig-2.pdf")
OUTPUT_FILE = Path("data_processed/population_projection_leipzig.csv")

TARGET_YEARS = {2018, 2020, 2025, 2030, 2035}


def normalize_number(value: str) -> int:
    return int(value.replace(" ", "").strip())


def extract_population_projection(pdf_path: Path) -> pd.DataFrame:
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[14]
        text = page.extract_text()

    if not text:
        raise ValueError("No text could be extracted from the population PDF.")

    for raw_line in text.splitlines():
        line = raw_line.strip()

        year_match = re.match(r"^(2018|2020|2025|2030|2035)\s+(.*)$", line)
        if not year_match:
            continue

        year = int(year_match.group(1))
        rest = year_match.group(2)

        numbers = re.findall(r"\d+", rest)

        # Expected order:
        # Leipzig V1: two number blocks
        # Leipzig V2: two number blocks
        # Saxony V1: four number blocks
        # Saxony V2: four number blocks
        if len(numbers) < 4:
            continue

        leipzig_variant_1 = normalize_number(numbers[0] + " " + numbers[1])
        leipzig_variant_2 = normalize_number(numbers[2] + " " + numbers[3])

        rows.append(
            {
                "year": year,
                "variant": "variant_1",
                "population": leipzig_variant_1,
            }
        )

        rows.append(
            {
                "year": year,
                "variant": "variant_2",
                "population": leipzig_variant_2,
            }
        )

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("No population values could be extracted from the PDF.")

    df = df.drop_duplicates(subset=["year", "variant"])
    df = df.sort_values(["variant", "year"])

    return df


def main() -> None:
    result = extract_population_projection(INPUT_FILE)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print(result)
    print("Rows written:", len(result))
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()