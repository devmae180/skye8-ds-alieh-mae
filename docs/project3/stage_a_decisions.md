# Stage A — Data Cleaning and Rule Baseline

## Data cleaning decisions

- The raw lots dataset contains 29,926 records.
- 300 duplicate `lot_id` values were found. Duplicate lot IDs were reduced to one record per lot, keeping the first occurrence.
- 200 lots reference cooperative IDs that are not present in the 120-cooperative register. These orphan references were excluded.
- Delivery dates use multiple formats. Dates were parsed using mixed-format parsing.
- `lot_weight_kg` and `defect_pct` are stored as strings in the raw data and were converted to numeric values.
- `rejected` values of `YES` and `NO` were converted to binary values 1 and 0.
- Rows with missing values in critical fields were removed.
- The data was sorted by delivery date before splitting.

## Time-based split

The data is split chronologically rather than randomly:

- 70% training
- 15% validation
- 15% final test

The final period remains untouched until model evaluation in Stage D.

## Published grading standard

The supplied grading standard was implemented as the incumbent rule.

A lot is rejected when:

- moisture > 8%
- defects > 6%
- bean count > 110 beans per 100g
- fermentation < 4 days

The fermentation standard contains `99` in the `reject_above` column, but the same row states that fermentation is a minimum of 4 days. Therefore, the documented minimum of 4 days was used rather than interpreting 99 as a rejection threshold.

## Baseline results

On the validation period:

- Precision: 0.1865
- Recall: 0.8186
- PR-AUC: 0.1806

The rejection prevalence is approximately 11.1%.

The always-accept baseline has 91.01% accuracy and 0% recall.

This proves that accuracy alone is misleading for this problem: a system can achieve high accuracy by accepting nearly every lot while detecting none of the rejected lots.

## Data-quality observation

The actual delivery dates extend beyond the date range described in the brief. The implementation uses the actual supplied delivery dates rather than silently deleting those records.
