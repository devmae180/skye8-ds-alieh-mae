from __future__ import annotations

import pandas as pd
import pytest


@pytest.fixture
def empty_frame() -> pd.DataFrame:
    return pd.DataFrame(columns=["id", "value"])


def test_empty_frame(empty_frame: pd.DataFrame) -> None:
    assert empty_frame.empty


def test_all_null_column() -> None:
    frame = pd.DataFrame({"value": [None, None, None]})
    assert frame["value"].isna().all()


def test_single_row_frame() -> None:
    frame = pd.DataFrame({"id": ["A"], "value": [10]})
    assert len(frame) == 1


@pytest.mark.parametrize(
    "timestamp",
    [
        "2025-01-01 12:00:00",
        "2025-01-01T12:00:00",
        1735732800,
    ],
)
def test_timestamp_format(timestamp: str | int) -> None:
    if isinstance(timestamp, int):
        result = pd.to_datetime(timestamp, unit="s")
    else:
        result = pd.to_datetime(timestamp)

    assert pd.notna(result)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("30kV", 30.0),
        ("45 kV", 45.0),
        ("60", 60.0),
    ],
)
def test_unit_suffixed_numeric(value: str, expected: float) -> None:
    cleaned = float(value.lower().replace("kv", "").strip())
    assert cleaned == expected


def test_duplicate_identifiers() -> None:
    frame = pd.DataFrame({"id": ["A", "A", "B"]})
    assert frame["id"].duplicated().sum() == 1


def test_no_duplicate_identifiers() -> None:
    frame = pd.DataFrame({"id": ["A", "B", "C"]})
    assert not frame["id"].duplicated().any()


def test_missing_identifier() -> None:
    frame = pd.DataFrame({"id": ["A", None, "C"]})
    assert frame["id"].isna().sum() == 1


def test_boolean_values() -> None:
    frame = pd.Series([True, False, True])
    assert frame.dtype == bool


def test_non_negative_duration() -> None:
    frame = pd.Series([0, 10, 180])
    assert (frame >= 0).all()


def test_valid_outage_order() -> None:
    start = pd.Timestamp("2025-01-01 10:00:00")
    end = pd.Timestamp("2025-01-01 11:00:00")
    assert end >= start


def test_invalid_outage_order() -> None:
    start = pd.Timestamp("2025-01-02 10:00:00")
    end = pd.Timestamp("2025-01-01 11:00:00")
    assert end < start


def test_valid_feeder_id() -> None:
    valid_ids = {"FD-001", "FD-002"}
    assert "FD-001" in valid_ids


def test_invalid_feeder_id() -> None:
    valid_ids = {"FD-001", "FD-002"}
    assert "FD-9288" not in valid_ids
