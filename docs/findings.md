# Grid Reliability Findings

## Summary

This analysis combines outage, feeder, customer, and weather data to support reliability planning for the coming rainy season. It uses outage frequency, duration, customer-minutes lost, and rainfall relationships to identify priority risks.

## Rainy-Season Risk

Daily rainfall has a correlation of **0.04647** with daily outage count and **0.08465** with mean outage duration. Both relationships are very weak positive correlations, suggesting that rainfall alone has a limited linear relationship with overall outage frequency and duration in this dataset.

By cause, **pole collapse (0.09944)** has the strongest rainfall-duration correlation, followed by **lightning strike (0.08497)** and **planned maintenance (0.08458)**. These relationships are still weak. **Transformer fault (-0.01544)** and **vegetation contact (-0.02770)** show little to no positive relationship with rainfall.

## Priority Feeders

The highest-priority feeders by customer-minutes lost are **FD-001 in Bamenda Main (62,104,472)**, **FD-013 in Bali (48,412,843)**, and **FD-006 in Mankon (45,882,980)**. Other high-priority feeders include **FD-011 in Bafut (40,778,616)** and **FD-030 in Fundong (38,523,641)**.

These feeders should receive priority inspection and preparation before the rainy season because their outages have resulted in high customer-minutes lost.

## Operational Recommendation

The distributor should prioritize inspection and maintenance of the highest customer-impact feeders before the rainy season. Particular attention should be given to causes with the strongest observed rainfall relationships, while recognizing that these relationships are weak.

## Performance Analysis

An index on `outages(feeder_id)` was added to support feeder-specific outage queries. The `EXPLAIN ANALYZE` test for `FD-001` still used a **Sequential Scan** after the index was added. The query found **84 matching rows** and removed **2,254 rows** by the filter, with an execution time of **1.437 ms**.

## Limitations

This analysis identifies associations and correlations. It does **not** establish that rainfall causes outages. Other factors, including equipment condition, maintenance, vegetation, network loading, and operational events, may influence outage frequency and duration. The results should therefore guide operational preparation rather than be interpreted as proof of causation.

## Query Traceability

- Monthly outage minutes: `sql/analytics.sql`
- SAIDI and SAIFI: `sql/analytics.sql`
- Customer-minutes lost: `sql/analytics.sql`
- Moving average: `sql/analytics.sql`
- Rainfall relationships: `sql/analytics.sql`
- Index performance: `EXPLAIN ANALYZE` performance analysis
