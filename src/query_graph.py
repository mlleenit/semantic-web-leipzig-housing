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
LIMIT 10
"""

    query_2 = prefixes + """
SELECT ?districtLabel ?warmRent ?stress ?status
WHERE {
    ?obs a lh:AffordabilityObservation ;
         lh:forDistrict ?district ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:hasWarmRent ?warmRent ;
         lh:hasHousingStressScore ?stress ;
         lh:hasAffordabilityStatus ?status .

    ?district rdfs:label ?districtLabel .

    FILTER(LANG(?districtLabel) = "de")
    FILTER(?stress > 0.45)
}
ORDER BY DESC(?stress)
"""

    query_3 = prefixes + """
SELECT ?status (COUNT(?obs) AS ?count)
WHERE {
    ?obs a lh:AffordabilityObservation ;
         lh:forGroup <https://example.org/leipzig-housing/group/students> ;
         lh:hasAffordabilityStatus ?status .
}
GROUP BY ?status
ORDER BY DESC(?count)
"""

    query_4 = prefixes + """
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

    run_query(g, "Query 1: Top 10 highest student housing stress districts", query_1)
    run_query(g, "Query 2: Districts above critical threshold for students", query_2)
    run_query(g, "Query 3: Affordability status counts for students", query_3)
    run_query(g, "Query 4: Official residential location classes by address count", query_4)


if __name__ == "__main__":
    main()