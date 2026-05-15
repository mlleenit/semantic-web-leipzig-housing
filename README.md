# semantic-web-leipzig-housing

Semantic Web project analyzing housing affordability in Leipzig using RDF-based urban data integration.

## Research Objective

This project investigates housing affordability for students in Leipzig by integrating heterogeneous urban datasets into a semantic knowledge graph.

Core research questions:

- Where in Leipzig is housing no longer affordable for students?
- To what extent does additional student income improve housing affordability?
- How can demographic projections contextualize future housing market pressure?

The project combines:
- rental market data
- district-level housing statistics
- residential location classifications
- student income scenarios
- official demographic projections

using RDF, SPARQL and semantic data modeling.

---

## Semantic Web Focus

The project demonstrates how heterogeneous urban datasets can be semantically integrated into a unified RDF-based knowledge graph.

The graph combines:
- affordability observations
- housing stock observations
- residential location observations
- demographic projections
- income scenarios

This enables cross-domain urban analysis through SPARQL queries and RDF-based knowledge representation.

---

## Technologies

- Python
- RDF / Turtle
- rdflib
- SPARQL
- pandas
- matplotlib
- Jupyter Notebook

---

## Project Structure

```text
data_raw/              # Raw input datasets
data_processed/        # Processed analysis datasets
rdf_output/            # Generated RDF graph
visual_output/         # Generated visualizations
src/                   # RDF generation and SPARQL scripts
notebooks/             # Exploratory analysis notebook
docs/                  # Methodology and documentation
```

---

## RDF Graph

Generate the RDF graph:

```bash
python src/build_rdf_graph.py
```

Run SPARQL analyses:

```bash
python src/query_graph.py
```

---

## Example Analyses

The project includes analyses such as:

- student housing affordability by district
- BAföG vs. Minijob affordability comparison
- housing stock vs. affordability
- residential location classification analysis
- demographic projection integration
- population growth analysis

---

## Visualizations

Generated visualizations include:

- top 15 districts with highest housing stress
- affordability comparison by income scenario
- housing stock vs affordability
- projected population development in Leipzig

---

## Results

The analysis shows that:
- all Leipzig districts fall into at least the critical affordability range for students relying solely on BAföG
- several central districts are classified as not affordable
- additional income significantly improves affordability
- demographic projections indicate continued population growth until 2035
- future housing pressure is likely to remain structurally high

---

## License

Hochschule für Technik, Wirtschaft und Kultur Leipzig project.