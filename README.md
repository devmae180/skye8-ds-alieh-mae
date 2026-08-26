[![CI](https://github.com/devmae180/skye8-ds-alieh-mae/actions/workflows/ci.yml/badge.svg)](https://github.com/devmae180/skye8-ds-alieh-mae/actions/workflows/ci.yml)

# Grid Reliability Analysis

A data engineering and analysis project for studying electricity grid
reliability using feeder, meter, and outage data.

## What the project does

The project:

- Cleans electricity grid datasets
- Checks data quality
- Stores the cleaned data in PostgreSQL
- Loads the data using Python
- Runs SQL analysis on the database
- Tests the data and application code
- Uses automated linting, formatting, type checking, and CI

## Data

The project uses three related datasets:

- **Feeders** — information about electricity feeders, locations,
  voltage, and customers served.
- **Meters** — customer meter information and electricity usage.
- **Outages** — outage events, affected feeders, timestamps, and
  outage duration.

The cleaned datasets contain:

- 37 feeders
- 11,000 meters
- 2,338 outages

## Database

The project uses PostgreSQL through Supabase.

The database contains three main tables:

```text
feeders
   |
   +---- meters
   |
   +---- outages