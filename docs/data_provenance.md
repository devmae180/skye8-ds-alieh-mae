# Weather Data Provenance

## Source

Historical daily weather data was sourced from the Open-Meteo Historical Weather API:

https://archive-api.open-meteo.com/v1/archive

The API was used to retrieve daily historical weather for the feeder coordinates contained in `data/raw/feeders.csv`.

## Request period

- Start date: 2024-01-01
- End date: 2026-06-30
- Timezone: UTC

## Weather variables

The following daily variables were requested:

- `precipitation_sum`
- `wind_speed_10m_max`
- `temperature_2m_max`

## Request parameters

Each request uses:

- latitude
- longitude
- start_date
- end_date
- daily weather variables
- timezone=UTC

The exact request URL is constructed by the `fetch_weather` function in:

`src/grid_reliability/weather.py`

## Retrieval date

Weather data was retrieved on:

2026-08-25

## Caching and reproducibility

Every successful API response is stored as a JSON file in the configured cache directory.

The cache filename contains:

- latitude
- longitude
- start date
- end date

When the same request is made again, the cached JSON response is returned instead of making another network request.

This allows the pipeline and tests to operate without network access after the initial weather download.

## Rate limiting

The client waits 1 second between successful network requests.

This deliberately keeps the client well below Open-Meteo's published allowance of approximately 10,000 calls per day.

## Retry policy

The client:

- retries HTTP 5xx server errors using exponential backoff;
- retries request timeouts using exponential backoff;
- does not retry HTTP 4xx client errors;
- reports the affected coordinates and date range when a request fails;
- rejects malformed JSON responses.

## Licence

Open-Meteo weather data is published under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence.

Attribution:

Weather data provided by Open-Meteo.com and its data providers, under CC BY 4.0.

## Reproduction

To reproduce the weather request, use the Open-Meteo Historical Weather API with the feeder latitude and longitude from `data/raw/feeders.csv`, the date range `2024-01-01` through `2026-06-30`, and the three variables listed above.

The resulting responses are cached locally so subsequent pipeline executions do not require network access.
