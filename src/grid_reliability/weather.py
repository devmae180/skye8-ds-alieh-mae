from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

# 1 request per second keeps our client comfortably below
# Open-Meteo's published allowance of roughly 10,000 calls/day.
REQUEST_DELAY_SECONDS = 1.0

MAX_RETRIES = 3
BACKOFF_SECONDS = 1.0


def fetch_weather(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    cache_dir: Path,
) -> dict[str, Any]:
    """Fetch and cache daily historical weather for one coordinate pair."""
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache_file = (
        cache_dir / f"{latitude:.6f}_{longitude:.6f}_{start_date}_{end_date}.json"
    )

    # Use the cached response instead of making another network request.
    if cache_file.exists():
        with cache_file.open("r", encoding="utf-8") as file:
            cached_data = json.load(file)

        if not isinstance(cached_data, dict):
            raise RuntimeError(
                f"Cached weather response is not a JSON object: {cache_file}"
            )

        return cached_data

    params: dict[str, str | float | list[str]] = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "precipitation_sum",
            "wind_speed_10m_max",
            "temperature_2m_max",
        ],
        "timezone": "UTC",
    }

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=30,
            )

            # 4xx errors are client/request errors.
            # They must not be retried.
            if 400 <= response.status_code < 500:
                raise RuntimeError(
                    f"Weather request failed for "
                    f"({latitude}, {longitude}) "
                    f"from {start_date} to {end_date}: "
                    f"HTTP {response.status_code}"
                )

            # Retry server errors.
            if response.status_code >= 500:
                if attempt == MAX_RETRIES:
                    raise RuntimeError(
                        f"Weather request failed for "
                        f"({latitude}, {longitude}) "
                        f"from {start_date} to {end_date}: "
                        f"HTTP {response.status_code} "
                        f"after {MAX_RETRIES} retries"
                    )

                time.sleep(BACKOFF_SECONDS * (2**attempt))
                continue

            try:
                data: dict[str, Any] = response.json()
            except ValueError as exc:
                raise RuntimeError(
                    f"Weather API returned malformed JSON for "
                    f"({latitude}, {longitude}) "
                    f"from {start_date} to {end_date}"
                ) from exc

            break

        except requests.Timeout as exc:
            if attempt == MAX_RETRIES:
                raise RuntimeError(
                    f"Weather request timed out for "
                    f"({latitude}, {longitude}) "
                    f"from {start_date} to {end_date} "
                    f"after {MAX_RETRIES} retries"
                ) from exc

            time.sleep(BACKOFF_SECONDS * (2**attempt))

        except requests.RequestException as exc:
            raise RuntimeError(
                f"Weather request failed for "
                f"({latitude}, {longitude}) "
                f"from {start_date} to {end_date}"
            ) from exc

    else:
        raise RuntimeError(
            f"Weather request failed for "
            f"({latitude}, {longitude}) "
            f"from {start_date} to {end_date}"
        )

    with cache_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    time.sleep(REQUEST_DELAY_SECONDS)

    return data
