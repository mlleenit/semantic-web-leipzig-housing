import pandas as pd

df = pd.read_excel(
    "data_raw/geo/Wohnlage_zum_Leipziger_Mietspiegel_2025-2027.xlsx"
)

df = df.rename(
    columns={
        "Straßenname": "street_name",
        "Hausnummer": "house_number",
        "Wohnlage zum Leipziger Mietspiegel 2025-2027": "residential_location",
        "Faktor": "location_factor",
    }
)

df.to_csv(
    "data_processed/official_residential_locations.csv",
    index=False
)