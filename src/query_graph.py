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
SELECT ?districtLabel ?groupLabel ?stress ?status
WHERE {
    ?obs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup ?group ;
         lh:hasHousingStressScore ?stress ;
         lh:hasAffordabilityStatus ?status .

    ?district rdfs:label ?districtLabel .
    ?group rdfs:label ?groupLabel .

    FILTER(LANG(?districtLabel) = "de")
    FILTER(LANG(?groupLabel) = "en")
    FILTER(?status = "structurally_excluded"@en)
}
ORDER BY DESC(?stress)
LIMIT 10
"""

    query_2 = prefixes + """
SELECT ?districtLabel ?stress ?status
WHERE {
    ?obs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:hasHousingStressScore ?stress ;
         lh:hasAffordabilityStatus ?status .

    ?district rdfs:label ?districtLabel .

    FILTER(LANG(?districtLabel) = "de")
}
ORDER BY DESC(?stress)
LIMIT 15
"""

    query_3 = prefixes + """
SELECT ?groupLabel ?status (COUNT(?obs) AS ?count)
WHERE {
    ?obs a lh:AffordabilityObservation ;
         lh:forGroup ?group ;
         lh:hasAffordabilityStatus ?status .

    ?group rdfs:label ?groupLabel .

    FILTER(LANG(?groupLabel) = "en")
}
GROUP BY ?groupLabel ?status
ORDER BY ?groupLabel DESC(?count)
"""

    query_4 = prefixes + """
SELECT ?districtLabel ?warmRent ?stress
WHERE {
    ?obs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup <https://example.org/leipzig-housing/group/apprentices> ;
         lh:hasWarmRent ?warmRent ;
         lh:hasHousingStressScore ?stress ;
         lh:hasAffordabilityStatus "not_affordable"@en .

    ?district rdfs:label ?districtLabel .

    FILTER(LANG(?districtLabel) = "de")
}
ORDER BY DESC(?stress)
LIMIT 15
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

    run_query(g, "Query 1: Top 10 structurally excluded combinations", query_1)
    run_query(g, "Query 2: Housing stress for students by district", query_2)
    run_query(g, "Query 3: Affordability status counts by social group", query_3)
    run_query(g, "Query 4: Not affordable districts for apprentices", query_4)
    run_query(g, "Query 5: Official residential location classes by address count", query_5)


if __name__ == "__main__":
    main()