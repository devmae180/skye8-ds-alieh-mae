from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

from grid_reliability.weather import fetch_weather

SAMPLE_WEATHER = {
    "latitude": 5.96,
    "longitude": 10.15,
    "daily": {
        "time": ["2024-01-01"],
        "precipitation_sum": [2.5],
        "wind_speed_10m_max": [15.2],
        "temperature_2m_max": [27.4],
    },
}


def test_fetch_weather_uses_cache(tmp_path: Path) -> None:
    """A cached response prevents a second network request."""
    with patch("grid_reliability.weather.requests.get") as mock_get:
        response = Mock()
        response.status_code = 200
        response.json.return_value = SAMPLE_WEATHER
        mock_get.return_value = response

        first_result = fetch_weather(
            latitude=5.96,
            longitude=10.15,
            start_date="2024-01-01",
            end_date="2024-01-01",
            cache_dir=tmp_path,
        )

        second_result = fetch_weather(
            latitude=5.96,
            longitude=10.15,
            start_date="2024-01-01",
            end_date="2024-01-01",
            cache_dir=tmp_path,
        )

    assert first_result == SAMPLE_WEATHER
    assert second_result == SAMPLE_WEATHER
    mock_get.assert_called_once()


def test_fetch_weather_retries_after_timeout(tmp_path: Path) -> None:
    """A timeout is retried until the maximum retry count is reached."""
    with (
        patch(
            "grid_reliability.weather.requests.get",
            side_effect=requests.Timeout,
        ) as mock_get,
        patch("grid_reliability.weather.time.sleep") as mock_sleep,
    ):
        with pytest.raises(RuntimeError, match="timed out"):
            fetch_weather(
                latitude=5.96,
                longitude=10.15,
                start_date="2024-01-01",
                end_date="2024-01-01",
                cache_dir=tmp_path,
            )

    assert mock_get.call_count == 4
    assert mock_sleep.call_count == 3


def test_fetch_weather_retries_500_then_succeeds(tmp_path: Path) -> None:
    """A server error is retried and succeeds on the next attempt."""
    first_response = Mock(status_code=500)
    second_response = Mock(status_code=200)
    second_response.json.return_value = SAMPLE_WEATHER

    with (
        patch(
            "grid_reliability.weather.requests.get",
            side_effect=[first_response, second_response],
        ) as mock_get,
        patch("grid_reliability.weather.time.sleep"),
    ):
        result = fetch_weather(
            latitude=5.96,
            longitude=10.15,
            start_date="2024-01-01",
            end_date="2024-01-01",
            cache_dir=tmp_path,
        )

    assert result == SAMPLE_WEATHER
    assert mock_get.call_count == 2


def test_fetch_weather_does_not_retry_400(tmp_path: Path) -> None:
    """A client error fails immediately without retrying."""
    response = Mock(status_code=400)

    with (
        patch(
            "grid_reliability.weather.requests.get",
            return_value=response,
        ) as mock_get,
        patch("grid_reliability.weather.time.sleep") as mock_sleep,
    ):
        with pytest.raises(RuntimeError, match="HTTP 400"):
            fetch_weather(
                latitude=5.96,
                longitude=10.15,
                start_date="2024-01-01",
                end_date="2024-01-01",
                cache_dir=tmp_path,
            )

    mock_get.assert_called_once()
    mock_sleep.assert_not_called()


def test_fetch_weather_rejects_malformed_json(tmp_path: Path) -> None:
    """A successful HTTP response with invalid JSON raises RuntimeError."""
    response = Mock(status_code=200)
    response.json.side_effect = ValueError("invalid JSON")

    with patch(
        "grid_reliability.weather.requests.get",
        return_value=response,
    ) as mock_get:
        with pytest.raises(RuntimeError, match="malformed JSON"):
            fetch_weather(
                latitude=5.96,
                longitude=10.15,
                start_date="2024-01-01",
                end_date="2024-01-01",
                cache_dir=tmp_path,
            )

    mock_get.assert_called_once()
