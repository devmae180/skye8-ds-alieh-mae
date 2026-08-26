from __future__ import annotations

from pathlib import Path

import pandas as pd
import psycopg

TABLES = (
    ("cleaned_feeders.csv", "feeders"),
    ("cleaned_meters.csv", "meters"),
    ("cleaned_outages.csv", "outages"),
)


def load_csv(
    connection: psycopg.Connection,
    csv_path: Path,
    table_name: str,
) -> None:
    """Load one cleaned CSV into PostgreSQL."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing cleaned file: {csv_path}")

    frame = pd.read_csv(csv_path)

    if frame.empty:
        return

    columns = list(frame.columns)
    column_list = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    query = (
        f"INSERT INTO {table_name} ({column_list}) "
        f"VALUES ({placeholders}) "
        f"ON CONFLICT DO NOTHING"
    )

    rows = [
        tuple(None if pd.isna(value) else value for value in row)
        for row in frame.itertuples(index=False, name=None)
    ]

    with connection.cursor() as cursor:
        cursor.executemany(query, rows)


def load_cleaned_data(
    connection: psycopg.Connection,
    data_dir: Path,
) -> None:
    """Load all cleaned relational datasets."""
    for filename, table_name in TABLES:
        load_csv(
            connection,
            data_dir / filename,
            table_name,
        )

    connection.commit()
