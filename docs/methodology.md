# Methodology

## Research Objective

This project analyzes housing affordability in the Leipzig rental market for different social groups.

Core research question:

> Where in Leipzig is housing no longer affordable for different social groups?

The analysis is based on a semantic data integration pipeline combining rental market data, social group modeling and income proxies.

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
- (to be extended with further sources)

---

## Data Pipeline

1. Raw data collection  
2. Data normalization and cleaning  
3. Affordability computation  
4. RDF graph construction  
5. SPARQL querying  
6. Analytical visualization  

---

## Limitations

- Income values are modeled as representative proxies  
- Rental data is based on offer prices, not contract rents  
- Flat size is fixed at 30 sqm for comparability  

---

## Data Validation

To ensure plausibility of the rental data, selected district-level rent values were cross-checked with the official Leipzig rent index (Mietspiegel Leipzig 2026).

The comparison confirmed that differences between districts such as Plagwitz and Reudnitz-Thonberg are minimal. For example, average rent per square meter differs by less than 0.1 EUR, resulting in nearly identical housing stress scores.

These small differences highlight that the ranking of districts in the analysis should not be interpreted as strict ordinal differences, but rather as approximate groupings within similar affordability levels.

This reflects a general limitation of using aggregated average rent data, where minor variations can lead to visible differences in rankings without representing meaningful real-world disparities.