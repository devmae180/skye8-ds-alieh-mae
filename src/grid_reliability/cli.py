from __future__ import annotations

import argparse
from pathlib import Path

from grid_reliability.database import get_connection
from grid_reliability.loader import load_cleaned_data


def load_data(raw_dir: Path) -> None:
    """Load cleaned project datasets into PostgreSQL."""
    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw data directory does not exist: {raw_dir}")

    data_dir = raw_dir.parent

    with get_connection() as connection:
        load_cleaned_data(connection, data_dir)

    print(f"Loaded data from {data_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="grid-reliability",
        description="Grid reliability data pipeline",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    load_parser = subparsers.add_parser(
        "load",
        help="Load project data into PostgreSQL",
    )

    load_parser.add_argument(
        "--raw",
        type=Path,
        required=True,
        help="Path to the raw data directory",
    )

    args = parser.parse_args()

    if args.command == "load":
        load_data(args.raw)


if __name__ == "__main__":
    main()
