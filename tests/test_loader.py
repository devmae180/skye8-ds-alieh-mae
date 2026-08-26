from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

from grid_reliability.loader import load_csv


def test_duplicate_rows_are_ignored(tmp_path: Path) -> None:
    csv_path = tmp_path / "feeders.csv"

    frame = pd.DataFrame(
        [
            {
                "feeder_id": "FD-001",
                "substation": "Bamenda Main",
                "town": "Bamenda",
                "voltage_kv": 30.0,
                "customers_served": 1000,
                "commissioned_year": 2020,
                "latitude": 5.96,
                "longitude": 10.15,
            }
        ]
    )

    frame.to_csv(csv_path, index=False)

    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value

    load_csv(connection, csv_path, "feeders")
    load_csv(connection, csv_path, "feeders")

    assert cursor.executemany.call_count == 2

    query = cursor.executemany.call_args.args[0]
    assert "ON CONFLICT DO NOTHING" in query
