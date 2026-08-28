# Grid Reliability Analysis

[![CI](https://github.com/devmae180/skye8-ds-alieh-mae/actions/workflows/ci.yml/badge.svg)](https://github.com/devmae180/skye8-ds-alieh-mae/actions/workflows/ci.yml)

A data analysis project for studying electricity outages and weather.
## What the project does

The project:

- Cleans electricity grid datasets
- Checks data quality
- Stores the cleaned data in PostgreSQL
- Loads data using Python
- Runs SQL analysis on the database
- Analyses outage frequency and duration
- Studies the relationship between rainfall and outages
- Tests the data and application code
- Uses automated linting, formatting, type checking, and CI

## Data

The project uses three main grid datasets:

- **Feeders** — information about electricity feeders, locations, voltage, substations, and customers served.
- **Meters** — customer meter information and electricity usage.
- **Outages** — outage events, affected feeders, timestamps, causes, and outage duration.

The cleaned datasets contain:

- 37 feeders
- 11,000 meters
- 2,338 outages

Weather data is obtained from Open-Meteo.

## Database

The project uses PostgreSQL through Supabase.

The database contains three main tables:

```text
feeders
   |
   +---- meters
   |
   +---- outages
```

The database schema is available in `sql/schema.sql`.

## Installation

Clone the repository and install the package:

```bash
git clone https://github.com/devmae180/skye8-ds-alieh-mae.git
cd skye8-ds-alieh-mae
python -m pip install -e ".[dev]"
```

## Quickstart

Run the project:

```bash
grid-reliability
```

Run the tests:

```bash
pytest
```

Run the code quality checks:

```bash
ruff check .
black --check .
mypy src
```

## Project Layout

```text
src/grid_reliability/     Python package and weather client
tests/                    Automated tests
sql/schema.sql            Database schema
sql/exercises.sql         25 SQL exercises
sql/analytics.sql         Reliability and weather analysis
sql/performance_analysis.sql
docs/data_provenance.md   Weather data provenance
docs/load_decisions.md    Data loading decisions
docs/data_quality.md      Data quality information
docs/findings.md          Reliability findings
scripts/                  Data loading scripts
notebooks/                Exploratory analysis
.github/workflows/        CI configuration
```

## Analysis Results

The analysis measures outage frequency, outage duration, customer impact, feeder reliability, and rainfall relationships.

The top feeders by customer-minutes lost in each substation are calculated in `sql/analytics.sql`.

The highest-ranked feeders include:

- FD-001 in Bamenda Main — 62,104,472 customer-minutes lost
- FD-013 in Bali — 48,412,843 customer-minutes lost
- FD-006 in Mankon — 45,882,980 customer-minutes lost
- FD-011 in Bafut — 40,778,616 customer-minutes lost
- FD-030 in Fundong — 38,523,641 customer-minutes lost

The overall correlation between rainfall and daily outage count is **0.04647**.

The correlation between rainfall and mean outage duration is **0.08465**.

The cause-level analysis shows different relationships between rainfall and outage duration. The strongest positive correlations were found for:

- Pole collapse — 0.09944
- Lightning strike — 0.08497
- Planned maintenance — 0.08458

The detailed findings and limitations are documented in `docs/findings.md`.

## Weather Data

Weather data is obtained from **Open-Meteo**.

The request URL, retrieval date, licence, and attribution information are recorded in:

`docs/data_provenance.md`

## Performance Analysis

A composite index on `feeder_id` and `start_ts` was added to support feeder-specific outage searches ordered by time.

The before and after `EXPLAIN ANALYZE` results are documented in:

`sql/performance_analysis.sql`

## SQL Analysis

The SQL work includes:

- 25 SQL exercises with increasing difficulty
- Filtering and aggregation
- `GROUP BY` and `HAVING`
- Four types of joins
- Subqueries and set operations
- NULL behaviour in aggregates
- Monthly outage analysis
- SAIDI and SAIFI
- Customer-minutes lost
- Window functions
- Seven-day moving averages
- Rainfall and outage relationships

The queries are available in:

- `sql/exercises.sql`
- `sql/analytics.sql`

## Continuous Integration

GitHub Actions runs the following checks:

- Package installation
- Ruff
- Black
- Mypy
- Pytest

The CI status is shown by the badge at the top of this README.

## Limitations

This analysis identifies relationships and correlations in the available data. It does **not** establish that rainfall causes outages.

Other factors, including equipment condition, maintenance, vegetation, network loading, and operational events, may also affect outage frequency and duration.

The findings should therefore be used to support reliability planning rather than treated as proof of causation.
