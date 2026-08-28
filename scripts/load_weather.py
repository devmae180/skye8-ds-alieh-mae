from pathlib import Path

from grid_reliability.database import get_connection
from grid_reliability.weather import fetch_weather

START_DATE = "2024-01-02"
END_DATE = "2026-06-30"
CACHE_DIR = Path("data/weather_cache")


def main() -> None:
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT feeder_id, latitude, longitude
                FROM feeders
                ORDER BY feeder_id
                """)
            feeders = cursor.fetchall()

        print(f"Found {len(feeders)} feeders.")

        inserted = 0

        for feeder_id, latitude, longitude in feeders:
            print(f"Fetching weather for {feeder_id}...")

            data = fetch_weather(
                latitude=float(latitude),
                longitude=float(longitude),
                start_date=START_DATE,
                end_date=END_DATE,
                cache_dir=CACHE_DIR,
            )

            daily = data.get("daily", {})
            dates = daily.get("time", [])
            precipitation = daily.get("precipitation_sum", [])
            wind = daily.get("wind_speed_10m_max", [])
            temperature = daily.get("temperature_2m_max", [])

            rows = [
                (
                    feeder_id,
                    dates[i],
                    precipitation[i],
                    wind[i],
                    temperature[i],
                )
                for i in range(len(dates))
            ]

            with conn.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO weather (
                        feeder_id,
                        weather_date,
                        precipitation_sum,
                        wind_speed_10m_max,
                        temperature_2m_max
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (feeder_id, weather_date) DO NOTHING
                    """,
                    rows,
                )

            inserted += len(rows)
            conn.commit()

            print(f"  Loaded {len(rows)} daily records.")

        print(f"Finished. Processed {inserted} weather records.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
