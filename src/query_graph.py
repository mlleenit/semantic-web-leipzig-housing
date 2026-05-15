from rdflib import Graph


GRAPH_PATH = "rdf_output/leipzig_housing_graph.ttl"


def run_query(graph: Graph, title: str, query: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

    results = graph.query(query)

    for row in results:
        values = [str(value) for value in row]
        print(" | ".join(values))


def main() -> None:
    g = Graph()
    g.parse(GRAPH_PATH, format="turtle")

    print("Graph loaded")
    print("Triples:", len(g))

    prefixes = """
PREFIX lh: <https://example.org/leipzig-housing/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

    query_1 = prefixes + """
SELECT ?districtLabel ?scenarioLabel ?warmRent ?income ?stress ?status
WHERE {
    ?obs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:forIncomeScenario ?scenario ;
         lh:hasWarmRent ?warmRent ;
         lh:hasMonthlyIncome ?income ;
         lh:hasHousingStressScore ?stress ;
         lh:hasAffordabilityStatus ?status .

    ?district rdfs:label ?districtLabel .
    ?scenario rdfs:label ?scenarioLabel .

    FILTER(LANG(?districtLabel) = "de")
}
ORDER BY ?districtLabel ?scenarioLabel
"""

    query_2 = prefixes + """
SELECT ?districtLabel ?scenarioLabel ?warmRent ?stress ?status
WHERE {
    ?obs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:forIncomeScenario ?scenario ;
         lh:hasWarmRent ?warmRent ;
         lh:hasHousingStressScore ?stress ;
         lh:hasAffordabilityStatus ?status .

    ?district rdfs:label ?districtLabel .
    ?scenario rdfs:label ?scenarioLabel .

    FILTER(LANG(?districtLabel) = "de")
    FILTER(?stress > 0.45)
}
ORDER BY DESC(?stress)
"""

    query_3 = prefixes + """
SELECT ?districtLabel ?stressBase ?statusBase ?stressWithMinijob ?statusWithMinijob
WHERE {
    ?baseObs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:forIncomeScenario <https://example.org/leipzig-housing/income_scenario/bafog_only> ;
         lh:hasHousingStressScore ?stressBase ;
         lh:hasAffordabilityStatus ?statusBase .

    ?minijobObs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:forIncomeScenario <https://example.org/leipzig-housing/income_scenario/bafog_plus_minijob> ;
         lh:hasHousingStressScore ?stressWithMinijob ;
         lh:hasAffordabilityStatus ?statusWithMinijob .

    ?district rdfs:label ?districtLabel .

    FILTER(LANG(?districtLabel) = "de")
}
ORDER BY DESC(?stressBase)
LIMIT 15
"""

    query_4 = prefixes + """
SELECT ?scenarioLabel ?status (COUNT(?obs) AS ?count)
WHERE {
    ?obs a lh:AffordabilityObservation ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:forIncomeScenario ?scenario ;
         lh:hasAffordabilityStatus ?status .

    ?scenario rdfs:label ?scenarioLabel .
}
GROUP BY ?scenarioLabel ?status
ORDER BY ?scenarioLabel DESC(?count)
"""

    query_5 = prefixes + """
SELECT ?locationClassLabel ?factor (COUNT(?obs) AS ?addressCount)
WHERE {
    ?obs a lh:ResidentialLocationObservation ;
         lh:hasResidentialLocationClass ?locationClass .

    ?locationClass rdfs:label ?locationClassLabel ;
                   lh:hasLocationFactor ?factor .

    FILTER(LANG(?locationClassLabel) = "de")
}
GROUP BY ?locationClassLabel ?factor
ORDER BY DESC(?addressCount)
"""

    query_6 = prefixes + """
SELECT ?districtLabel ?housingUnits ?stress ?status
WHERE {
    ?stockObs a lh:HousingStockObservation ;
         lh:forDistrict ?district ;
         lh:inYear 2024 ;
         lh:hasHousingUnits ?housingUnits .

    ?affObs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:forIncomeScenario <https://example.org/leipzig-housing/income_scenario/bafog_only> ;
         lh:hasHousingStressScore ?stress ;
         lh:hasAffordabilityStatus ?status .

    ?district rdfs:label ?districtLabel .

    FILTER(LANG(?districtLabel) = "de")
}
ORDER BY DESC(?housingUnits)
LIMIT 15
"""

    query_7 = prefixes + """
SELECT ?year ?variantLabel ?population
WHERE {
    ?obs a lh:PopulationObservation ;
         lh:inYear ?year ;
         lh:hasPopulation ?population ;
         lh:hasVariant ?variant .

    ?variant rdfs:label ?variantLabel .
}
ORDER BY ?year ?variantLabel
"""

    query_8 = prefixes + """
SELECT ?districtLabel ?stress ?status ?population2035
WHERE {
    ?affObs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:forIncomeScenario <https://example.org/leipzig-housing/income_scenario/bafog_only> ;
         lh:hasHousingStressScore ?stress ;
         lh:hasAffordabilityStatus ?status .

    ?district rdfs:label ?districtLabel .

    ?popObs a lh:PopulationObservation ;
            lh:inYear 2035 ;
            lh:hasPopulation ?population2035 ;
            lh:hasVariant <https://example.org/leipzig-housing/population_variant/variant_1> .

    FILTER(LANG(?districtLabel) = "de")
}
ORDER BY DESC(?stress)
LIMIT 15
"""

    run_query(g, "Query 1: Student affordability by district and income scenario", query_1)
    run_query(g, "Query 2: Critical districts by scenario", query_2)
    run_query(g, "Query 3: BAföG vs Minijob comparison (MOST IMPORTANT)", query_3)
    run_query(g, "Query 4: Status distribution per scenario", query_4)
    run_query(g, "Query 5: Residential location classes", query_5)
    run_query(g, "Query 6: Housing stock and student affordability", query_6)
    run_query(g, "Query 7: Leipzig population projection by variant", query_7)
    run_query(g, "Query 8: Housing stress and projected Leipzig population growth", query_8)


if __name__ == "__main__":
    main()