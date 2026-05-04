import pandas as pd

rent_values = {
    "althen_kleinpoesna": 8.94,
    "altlindenau": 10.29,
    "anger_crottendorf": 9.78,
    "baalsdorf": 9.31,
    "boehlitz_ehrenberg": 9.83,
    "burghausen_rueckmarsdorf": 10.60,
    "connewitz": 10.62,
    "doelitz_doesen": 9.42,
    "engelsdorf": 10.82,
    "eutritzsch": 10.99,
    "gohlis_mitte": 10.43,
    "gohlis_nord": 9.44,
    "gohlis_sued": 10.74,
    "grosszschocher": 9.57,
    "gruenau_mitte": 8.35,
    "gruenau_nord": 8.29,
    "gruenau_ost": 7.94,
    "gruenau_siedlung": 7.73,
    "hartmannsdorf_knautnaundorf": 11.24,
    "heiterblick": 8.84,
    "holzhausen": 10.02,
    "kleinzschocher": 9.90,
    "knautkleeberg_knauthain": 9.28,
    "lausen_gruenau": 8.76,
    "leutzsch": 10.41,
    "liebertwolkwitz": 9.43,
    "lindenau": 10.09,
    "lindenthal": 9.54,
    "loessnig": 8.53,
    "luetzschena_stahmeln": 8.54,
    "marienbrunn": 10.04,
    "meusdorf": 10.39,
    "miltitz": 10.14,
    "mockau_nord": 9.23,
    "mockau_sued": 9.80,
    "moeckern": 10.63,
    "moelkau": 10.56,
    "neulindenau": 11.43,
    "neustadt_neuschoenefeld": 10.77,
    "paunsdorf": 8.93,
    "plagwitz": 10.72,
    "plaussig_portitz": 10.17,
    "probstheida": 10.07,
    "reudnitz_thonberg": 10.80,
    "schleussig": 10.13,
    "schoenau": 7.87,
    "schoenefeld_abtnaundorf": 9.46,
    "schoenefeld_ost": 8.60,
    "seehausen": 10.84,
    "sellerhausen_stuenz": 9.98,
    "stoetteritz": 10.85,
    "suedvorstadt": 10.62,
    "thekla": 8.99,
    "volkmarsdorf": 10.01,
    "wahren": 9.15,
    "wiederitzsch": 9.72,
    "zentrum": 11.43,
    "zentrum_nord": 12.50,
    "zentrum_nordwest": 11.63,
    "zentrum_ost": 13.11,
    "zentrum_sued": 11.78,
    "zentrum_suedost": 12.76,
    "zentrum_west": 11.81
}

records = []

for district_id, rent in rent_values.items():
    records.append({
        "observation_id": f"rent_{district_id}_2026",
        "district_id": district_id,
        "year": 2026,
        "offer_rent_per_sqm": rent,
        "flat_size_sqm": 30,
        "utilities_eur": 120,
        "source_id": "wohnungsboerse_2026",
        "notes": "Offer rent per sqm from Wohnungsboerse Leipzig"
    })

df = pd.DataFrame(records)
df.to_csv("data_raw/rents/rent_observations.csv", index=False)

print(df.head())
print("Rows written:", len(df))