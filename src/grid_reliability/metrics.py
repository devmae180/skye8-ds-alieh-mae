from __future__ import annotations

import pandas as pd


def calculate_average_outage_duration(outages: pd.DataFrame) -> float:
    """Calculate the average outage duration."""
    if outages.empty:
        return 0.0

    return float(outages["duration_min"].mean())


def calculate_outage_frequency(outages: pd.DataFrame) -> float:
    """Calculate the average number of outages per feeder."""
    if outages.empty:
        return 0.0

    return float(outages.groupby("feeder_id").size().mean())


def calculate_customers_affected(
    outages: pd.DataFrame,
) -> int:
    """Calculate the total number of customers affected."""
    if outages.empty:
        return 0

    return int(outages["customers_affected"].sum())
