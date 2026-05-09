# Methodology

## Research Objective

This project analyzes housing affordability in the Leipzig rental market for different social groups.

Core research question:

> Where in Leipzig is housing no longer affordable for different social groups?

The analysis is based on a semantic data integration pipeline combining rental market data, social group modeling and income proxies.

In addition to the base scenario, a second income scenario is introduced.

This allows the comparison between:
- students relying solely on BAföG
- students combining BAföG with additional income from part-time employment

Extended research question:

> To what extent does additional student income (e.g. via a Minijob) improve housing affordability in Leipzig?

---

## Affordability Model

Housing affordability is operationalized using a housing stress index:

housing_stress_score = warm_rent / monthly_income

Interpretation:

- <= 0.30 → affordable  
- <= 0.45 → critical  
- <= 0.60 → not_affordable  
- > 0.60 → structurally_excluded  

Warm rent is calculated as:

warm_rent = (offer_rent_per_sqm * 30 sqm) + 120 EUR utilities

Two affordability scenarios are computed:

1. Base scenario:
   monthly_income = BAföG

2. Extended scenario:
   monthly_income = BAföG + additional student income

The housing stress score is calculated separately for both scenarios.

---

## Social Groups

The analysis models the following social groups:

- students  

### Scope Definition

This analysis focuses exclusively on students as the primary social group.

Reason:

- Students represent a large and relevant population in Leipzig
- Their income situation can be modeled in a standardized way (BAföG rates)
- They are highly dependent on the rental market

Other groups (e.g. apprentices) were excluded due to:

- high variability in income (depending on profession and training year)
- additional financial support mechanisms (e.g. BAB, housing benefits)
- heterogeneous living situations

Focusing on students ensures a consistent and comparable affordability model.

---

## Income Modeling Decisions

### Students

Students are modeled using the BAföG maximum support rate for independently living students.

Value used:

- 992 EUR/month

Source:

- BAföG (Federal Training Assistance Act)  
  https://www.bafög.de/bafoeg/de/das-bafoeg-alle-infos-auf-einen-blick/foerderungsarten-und-foerderungshoehe/was-sind-bedarfssaetze-und-wie-hoch-sind-sie/was-sind-bedarfssaetze-und-wie-hoch-sind-sie.html  
- Deutsches Studierendenwerk (2024 reform rates)  
  https://www.studentenwerk-leipzig.de/bafoeg-finanzierung/bafoeg-reform-2024-25/

Justification:

The research focuses on access to the rental housing market. Therefore, students are modeled as living independently, since only this group actively participates in the housing market.

Students living with their parents are excluded from the affordability model, as they do not generate independent housing demand.

---

### Additional Student Income Scenario

A second income scenario is introduced to reflect the common situation where students supplement their income through part-time work.

Value used:

- 603 EUR/month

Source:

- Minijob-Zentrale  
  https://www.minijob-zentrale.de/DE/die-minijobs/studenten

Justification:

This value represents the maximum regular monthly income for marginal employment (Minijob) without exceeding the official earnings threshold.

The scenario does not assume that all students work, but models a realistic upper-bound case to evaluate whether additional income is sufficient to improve housing affordability.

This enables a comparative analysis between a base income scenario and an extended income scenario.

---

### Excluded Groups

Citizen benefit recipients were considered but ultimately excluded due to the non-uniform structure of benefits.

Including this group would introduce inconsistencies in the affordability model, as their effective housing costs differ significantly depending on individual entitlement and local policy.

---

## Data Sources

### Rental Data

- Wohnungsboerse Leipzig Mietspiegel 2026 (offer rents per district)

### Geographic Data

- Leipzig district dataset (63 official districts)  
  https://www.leipzig.de/mein-stadtteil

### Residential Location Data

- Official Leipzig rent index (Wohnlage classification)

### Income Data

- BAföG rates (students)  
- Minijob-Zentrale (student employment income limits)

---

## Data Pipeline

1. Raw data collection  
2. Data normalization and cleaning  
3. Affordability computation (multiple income scenarios)  
4. RDF graph construction  
5. SPARQL querying  
6. Analytical visualization  

Each district is evaluated under multiple income scenarios, enabling comparative analysis of affordability under different financial conditions.

---

## Limitations

- Income values are modeled as representative proxies  
- Rental data is based on offer prices, not contract rents  
- Flat size is fixed at 30 sqm for comparability  
- The additional income scenario assumes maximum allowed Minijob earnings and therefore represents an optimistic case  

---

## Data Validation

To ensure plausibility of the rental data, selected district-level rent values were cross-checked with the official Leipzig rent index (Mietspiegel Leipzig 2026).

The comparison confirmed that differences between districts such as Plagwitz and Reudnitz-Thonberg are minimal. For example, average rent per square meter differs by less than 0.1 EUR, resulting in nearly identical housing stress scores.

These small differences highlight that the ranking of districts in the analysis should not be interpreted as strict ordinal differences, but rather as approximate groupings within similar affordability levels.

This reflects a general limitation of using aggregated average rent data, where minor variations can lead to visible differences in rankings without representing meaningful real-world disparities.

---

## Results and Interpretation

The analysis reveals a clear pattern of housing affordability constraints for students in Leipzig.

In the base scenario (BAföG only), all districts fall into at least the "critical" affordability range, with several central districts reaching "not affordable" levels. In particular, districts such as Zentrum-Ost, Zentrum-Südost and Zentrum-Nord exhibit housing stress scores above 0.5, indicating severe financial pressure.

When introducing additional income through a Minijob, affordability improves significantly across all districts. The majority of districts shift into the "affordable" category, demonstrating the strong impact of increased income on housing stress.

However, the results also show that even with additional income, certain central districts remain problematic. For example, Zentrum-Ost and Zentrum-Südost still fall into the "critical" category.

This indicates that structural affordability issues persist in high-demand urban areas, and that additional income alone is not sufficient to fully offset high rental costs in these locations.

The visualization results confirm the findings from the SPARQL analysis.

The status distribution clearly shows that in the BAföG-only scenario, no district is classified as affordable, with the majority falling into the critical category.

In contrast, the Minijob scenario significantly shifts the distribution towards affordability, with most districts becoming affordable.

The comparison of the top 15 districts with the highest housing stress further illustrates that although additional income reduces stress levels substantially, central districts such as Zentrum-Ost and Zentrum-Südost remain within the critical range.

This highlights that increased income improves affordability, but does not fully compensate for high rental costs in central urban areas.