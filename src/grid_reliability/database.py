from __future__ import annotations

import os
from pathlib import Path

import psycopg


def get_connection() -> psycopg.Connection:
    """Create a PostgreSQL connection from DATABASE_URL."""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is required")

    return psycopg.connect(database_url)


def run_schema(
    connection: psycopg.Connection,
    schema_path: Path,
) -> None:
    """Create the database schema from a SQL file."""
    sql = schema_path.read_text(encoding="utf-8")
    connection.execute(sql)
    connection.commit()
