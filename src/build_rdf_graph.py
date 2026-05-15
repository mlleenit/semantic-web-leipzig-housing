from pathlib import Path
from urllib.parse import quote

import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import XSD, DCTERMS


BASE = "https://example.org/leipzig-housing/"
LH = Namespace(BASE)
SCHEMA = Namespace("https://schema.org/")


def uri(local_id: str) -> URIRef:
    return URIRef(BASE + quote(str(local_id).strip().replace(" ", "_")))


def add_decimal(graph: Graph, subject: URIRef, predicate: URIRef, value) -> None:
    graph.add((subject, predicate, Literal(float(value), datatype=XSD.decimal)))


def add_integer(graph: Graph, subject: URIRef, predicate: URIRef, value) -> None:
    graph.add((subject, predicate, Literal(int(value), datatype=XSD.integer)))


def main() -> None:
    districts = pd.read_csv("data_raw/geo/districts.csv")
    social_groups = pd.read_csv("data_raw/social/social_groups.csv")
    incomes = pd.read_csv("data_raw/income/income_observations.csv")
    rents = pd.read_csv("data_raw/rents/rent_observations.csv")
    affordability = pd.read_csv("data_processed/affordability_observations.csv")
    residential_locations = pd.read_csv("data_processed/official_residential_locations.csv")
    housing_stock = pd.read_csv("data_processed/housing_stock_observations.csv")

    output_dir = Path("rdf_output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "leipzig_housing_graph.ttl"

    g = Graph()

    g.bind("lh", LH)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    g.bind("dcterms", DCTERMS)
    g.bind("schema", SCHEMA)

    # Classes
    classes = [
        "District",
        "SocialGroup",
        "IncomeScenario",
        "RentObservation",
        "IncomeObservation",
        "AffordabilityObservation",
        "ResidentialLocationObservation",
        "HousingStockObservation",
        "ResidentialLocationClass",
        "DataSource",
    ]

    for class_name in classes:
        class_uri = LH[class_name]
        g.add((class_uri, RDF.type, RDFS.Class))
        g.add((class_uri, RDFS.label, Literal(class_name, lang="en")))

    # Properties
    object_properties = [
        "forDistrict",
        "forGroup",
        "forIncomeScenario",
        "basedOnSource",
        "hasResidentialLocationClass",
    ]

    datatype_properties = [
        "districtName",
        "city",
        "country",
        "inYear",
        "hasOfferRentPerSqm",
        "hasFlatSizeSqm",
        "hasUtilities",
        "hasWarmRent",
        "hasMonthlyIncome",
        "hasHousingStressScore",
        "hasAffordabilityStatus",
        "streetName",
        "houseNumber",
        "hasLocationFactor",
        "hasHousingUnits",
    ]

    for prop in object_properties + datatype_properties:
        prop_uri = LH[prop]
        g.add((prop_uri, RDF.type, RDF.Property))
        g.add((prop_uri, RDFS.label, Literal(prop, lang="en")))

    # Domain and range definitions
    # Domains are only used where a property is specific to one observation type.
    # For shared properties, only ranges are defined to avoid unintended RDFS inference.

    g.add((LH.forDistrict, RDFS.range, LH.District))
    g.add((LH.forGroup, RDFS.range, LH.SocialGroup))
    g.add((LH.forIncomeScenario, RDFS.range, LH.IncomeScenario))
    g.add((LH.basedOnSource, RDFS.range, LH.DataSource))

    g.add((LH.hasResidentialLocationClass, RDFS.domain, LH.ResidentialLocationObservation))
    g.add((LH.hasResidentialLocationClass, RDFS.range, LH.ResidentialLocationClass))

    g.add((LH.hasHousingStressScore, RDFS.domain, LH.AffordabilityObservation))
    g.add((LH.hasHousingStressScore, RDFS.range, XSD.decimal))

    g.add((LH.hasAffordabilityStatus, RDFS.domain, LH.AffordabilityObservation))
    g.add((LH.hasAffordabilityStatus, RDFS.range, XSD.string))

    g.add((LH.hasOfferRentPerSqm, RDFS.range, XSD.decimal))
    g.add((LH.hasFlatSizeSqm, RDFS.range, XSD.decimal))
    g.add((LH.hasUtilities, RDFS.range, XSD.decimal))
    g.add((LH.hasWarmRent, RDFS.range, XSD.decimal))
    g.add((LH.hasMonthlyIncome, RDFS.range, XSD.decimal))
    g.add((LH.hasLocationFactor, RDFS.range, XSD.decimal))
    g.add((LH.inYear, RDFS.range, XSD.integer))
    g.add((LH.hasHousingUnits, RDFS.domain, LH.HousingStockObservation))
    g.add((LH.hasHousingUnits, RDFS.range, XSD.integer))

    g.add((LH.districtName, RDFS.range, XSD.string))
    g.add((LH.city, RDFS.range, XSD.string))
    g.add((LH.country, RDFS.range, XSD.string))
    g.add((LH.streetName, RDFS.range, XSD.string))
    g.add((LH.houseNumber, RDFS.range, XSD.string))

    # Data sources
    sources = [
        (
            LH["source/wohnungsboerse_2026"],
            "Wohnungsboerse Leipzig Mietspiegel 2026",
            "Publicly available offer rent data by Leipzig district, status April 2026.",
        ),
        (
            LH["source/bafoeg_2024"],
            "BAföG maximum support rate",
            "Federal student support rate used as income proxy for independently living students.",
        ),
        (
            LH["source/bafoeg_2024_minijob_2026"],
            "BAföG plus Minijob income scenario",
            "Combined income scenario using BAföG maximum support rate and the 2026 Minijob earnings threshold.",
        ),
        (
            LH["source/leipzig_mietspiegel_2025_2027"],
            "Leipziger Mietspiegel 2025-2027",
            "Official qualified rent index and residential location classification by the City of Leipzig.",
        ),
        (
            LH["source/leipzig_housing_stock"],
            "Leipzig housing stock statistics",
            "Official Leipzig statistics on the number of housing units by district for 2020 to 2024.",
        ),
    ]

    for source_uri, title, description in sources:
        g.add((source_uri, RDF.type, LH.DataSource))
        g.add((source_uri, DCTERMS.title, Literal(title, lang="en")))
        g.add((source_uri, DCTERMS.description, Literal(description, lang="en")))

    # Districts
    for _, row in districts.iterrows():
        district = uri(f"district/{row['district_id']}")
        g.add((district, RDF.type, LH.District))
        g.add((district, RDFS.label, Literal(row["district_name"], lang="de")))
        g.add((district, LH.districtName, Literal(row["district_name"], lang="de")))
        g.add((district, LH.city, Literal(row["city"], lang="en")))
        g.add((district, LH.country, Literal(row["country"], lang="en")))

        if pd.notna(row.get("dbpedia_uri")) and str(row.get("dbpedia_uri")).strip():
            g.add((district, RDFS.seeAlso, URIRef(str(row["dbpedia_uri"]).strip())))

        if pd.notna(row.get("linked_geo_uri")) and str(row.get("linked_geo_uri")).strip():
            g.add((district, RDFS.seeAlso, URIRef(str(row["linked_geo_uri"]).strip())))

    # Social groups
    for _, row in social_groups.iterrows():
        group = uri(f"group/{row['group_id']}")
        g.add((group, RDF.type, LH.SocialGroup))
        g.add((group, RDFS.label, Literal(row["group_label_en"], lang="en")))
        g.add((group, RDFS.label, Literal(row["group_label_de"], lang="de")))
        g.add((group, DCTERMS.description, Literal(row["description"], lang="en")))

    # Income scenarios
    for scenario_id in incomes["income_scenario_id"].dropna().unique():
        scenario = uri(f"income_scenario/{scenario_id}")
        g.add((scenario, RDF.type, LH.IncomeScenario))
        g.add((scenario, RDFS.label, Literal(str(scenario_id), lang="en")))

    # Income observations
    for _, row in incomes.iterrows():
        obs = uri(f"income_observation/{row['observation_id']}")
        group = uri(f"group/{row['group_id']}")
        scenario = uri(f"income_scenario/{row['income_scenario_id']}")
        source = LH[f"source/{row['source_id']}"]

        g.add((obs, RDF.type, LH.IncomeObservation))
        g.add((obs, LH.forGroup, group))
        g.add((obs, LH.forIncomeScenario, scenario))
        add_integer(g, obs, LH.inYear, row["year"])
        add_decimal(g, obs, LH.hasMonthlyIncome, row["monthly_income_eur"])
        g.add((obs, LH.basedOnSource, source))

        if pd.notna(row.get("notes")):
            g.add((obs, RDFS.comment, Literal(str(row["notes"]).strip(), lang="en")))

    # Rent observations
    for _, row in rents.iterrows():
        obs = uri(f"rent_observation/{row['observation_id']}")
        district = uri(f"district/{row['district_id']}")
        source = LH[f"source/{row['source_id']}"]

        warm_rent = row["offer_rent_per_sqm"] * row["flat_size_sqm"] + row["utilities_eur"]

        g.add((obs, RDF.type, LH.RentObservation))
        g.add((obs, LH.forDistrict, district))
        add_integer(g, obs, LH.inYear, row["year"])
        add_decimal(g, obs, LH.hasOfferRentPerSqm, row["offer_rent_per_sqm"])
        add_decimal(g, obs, LH.hasFlatSizeSqm, row["flat_size_sqm"])
        add_decimal(g, obs, LH.hasUtilities, row["utilities_eur"])
        add_decimal(g, obs, LH.hasWarmRent, warm_rent)
        g.add((obs, LH.basedOnSource, source))

        if pd.notna(row.get("notes")):
            g.add((obs, RDFS.comment, Literal(str(row["notes"]).strip(), lang="en")))

    # Housing stock observations
    for _, row in housing_stock.iterrows():
        obs = uri(f"housing_stock_observation/{row['district_id']}_{row['year']}")
        district = uri(f"district/{row['district_id']}")
        source = LH[f"source/{row['source_id']}"]

        g.add((obs, RDF.type, LH.HousingStockObservation))
        g.add((obs, LH.forDistrict, district))
        add_integer(g, obs, LH.inYear, row["year"])
        add_integer(g, obs, LH.hasHousingUnits, row["housing_units"])
        g.add((obs, LH.basedOnSource, source))        

    # Affordability observations
    for _, row in affordability.iterrows():
        obs = uri(f"affordability_observation/{row['observation_id']}")
        district = uri(f"district/{row['district_id']}")
        group = uri(f"group/{row['group_id']}")
        scenario = uri(f"income_scenario/{row['income_scenario_id']}")
        rent_source = LH[f"source/{row['rent_source_id']}"]
        income_source = LH[f"source/{row['income_source_id']}"]

        g.add((obs, RDF.type, LH.AffordabilityObservation))
        g.add((obs, LH.forDistrict, district))
        g.add((obs, LH.forGroup, group))
        g.add((obs, LH.forIncomeScenario, scenario))
        add_integer(g, obs, LH.inYear, row["year"])
        add_decimal(g, obs, LH.hasOfferRentPerSqm, row["offer_rent_per_sqm"])
        add_decimal(g, obs, LH.hasFlatSizeSqm, row["flat_size_sqm"])
        add_decimal(g, obs, LH.hasUtilities, row["utilities_eur"])
        add_decimal(g, obs, LH.hasWarmRent, row["warm_rent_eur"])
        add_decimal(g, obs, LH.hasMonthlyIncome, row["monthly_income_eur"])
        add_decimal(g, obs, LH.hasHousingStressScore, row["housing_stress_score"])
        g.add((obs, LH.hasAffordabilityStatus, Literal(row["affordability_status"], lang="en")))
        g.add((obs, LH.basedOnSource, rent_source))
        g.add((obs, LH.basedOnSource, income_source))

    # Residential location classes
    for location_name, factor in (
        residential_locations[["residential_location", "location_factor"]]
        .drop_duplicates()
        .sort_values("residential_location")
        .itertuples(index=False)
    ):
        class_id = (
            str(location_name)
            .lower()
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
            .replace(" - ", "_")
            .replace(" ", "_")
            .replace("-", "_")
        )

        location_class = uri(f"residential_location_class/{class_id}")

        g.add((location_class, RDF.type, LH.ResidentialLocationClass))
        g.add((location_class, RDFS.label, Literal(str(location_name), lang="de")))
        add_decimal(g, location_class, LH.hasLocationFactor, factor)
        g.add((location_class, LH.basedOnSource, LH["source/leipzig_mietspiegel_2025_2027"]))

    # Residential location observations
    for idx, row in residential_locations.iterrows():
        class_id = (
            str(row["residential_location"])
            .lower()
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
            .replace(" - ", "_")
            .replace(" ", "_")
            .replace("-", "_")
        )

        obs = uri(f"residential_location_observation/{idx + 1}")
        location_class = uri(f"residential_location_class/{class_id}")

        g.add((obs, RDF.type, LH.ResidentialLocationObservation))
        g.add((obs, LH.streetName, Literal(row["street_name"], lang="de")))
        g.add((obs, LH.houseNumber, Literal(str(row["house_number"]))))
        g.add((obs, LH.hasResidentialLocationClass, location_class))
        add_decimal(g, obs, LH.hasLocationFactor, row["location_factor"])
        g.add((obs, LH.basedOnSource, LH["source/leipzig_mietspiegel_2025_2027"]))

    g.serialize(destination=output_file, format="turtle")

    print("RDF graph created")
    print("Triples:", len(g))
    print("Saved:", output_file)


if __name__ == "__main__":
    main()