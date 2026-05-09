from pathlib import Path

import pandas as pd


AFFORDABLE_THRESHOLD = 0.30
CRITICAL_THRESHOLD = 0.45
EXCLUDED_THRESHOLD = 0.60


def classify_affordability(score: float) -> str:
    if score <= AFFORDABLE_THRESHOLD:
        return "affordable"
    if score <= CRITICAL_THRESHOLD:
        return "critical"
    if score <= EXCLUDED_THRESHOLD:
        return "not_affordable"
    return "structurally_excluded"


def main() -> None:
    rents_path = Path("data_raw/rents/rent_observations.csv")
    income_path = Path("data_raw/income/income_observations.csv")
    output_path = Path("data_processed/affordability_observations.csv")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    rents = pd.read_csv(rents_path)
    incomes = pd.read_csv(income_path)

    required_rent_columns = {
        "district_id",
        "year",
        "offer_rent_per_sqm",
        "flat_size_sqm",
        "utilities_eur",
        "source_id",
    }

    required_income_columns = {
        "group_id",
        "income_scenario_id",
        "monthly_income_eur",
        "source_id",
    }

    missing_rent_columns = required_rent_columns - set(rents.columns)
    missing_income_columns = required_income_columns - set(incomes.columns)

    if missing_rent_columns:
        raise ValueError(f"Missing rent columns: {sorted(missing_rent_columns)}")

    if missing_income_columns:
        raise ValueError(f"Missing income columns: {sorted(missing_income_columns)}")

    records = []

    for _, rent_row in rents.iterrows():
        warm_rent = (
            rent_row["offer_rent_per_sqm"] * rent_row["flat_size_sqm"]
            + rent_row["utilities_eur"]
        )

        for _, income_row in incomes.iterrows():
            stress_score = warm_rent / income_row["monthly_income_eur"]
            status = classify_affordability(stress_score)

            records.append(
                {
                    "observation_id": (
                        f"affordability_"
                        f"{rent_row['district_id']}_"
                        f"{income_row['group_id']}_"
                        f"{income_row['income_scenario_id']}_"
                        f"{rent_row['year']}"
                    ),
                    "district_id": rent_row["district_id"],
                    "group_id": income_row["group_id"],
                    "income_scenario_id": income_row["income_scenario_id"],
                    "year": int(rent_row["year"]),
                    "offer_rent_per_sqm": round(rent_row["offer_rent_per_sqm"], 2),
                    "flat_size_sqm": int(rent_row["flat_size_sqm"]),
                    "utilities_eur": round(rent_row["utilities_eur"], 2),
                    "warm_rent_eur": round(warm_rent, 2),
                    "monthly_income_eur": round(income_row["monthly_income_eur"], 2),
                    "housing_stress_score": round(stress_score, 3),
                    "affordability_status": status,
                    "rent_source_id": rent_row["source_id"],
                    "income_source_id": income_row["source_id"],
                }
            )

    affordability = pd.DataFrame(records)
    affordability.to_csv(output_path, index=False)

    print(affordability.head())
    print("Rows written:", len(affordability))
    print("Saved:", output_path)


if __name__ == "__main__":
    main()