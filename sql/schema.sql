CREATE TABLE IF NOT EXISTS feeders (
    feeder_id TEXT PRIMARY KEY,
    substation TEXT NOT NULL,
    town TEXT NOT NULL,
    voltage_kv NUMERIC(6, 2) CHECK (voltage_kv > 0),
    customers_served INTEGER NOT NULL CHECK (customers_served >= 0),
    commissioned_year INTEGER CHECK (
        commissioned_year BETWEEN 1900 AND 2100
    ),
    latitude NUMERIC(9, 6) NOT NULL CHECK (
        latitude BETWEEN -90 AND 90
    ),
    longitude NUMERIC(9, 6) NOT NULL CHECK (
        longitude BETWEEN -180 AND 180
    )
);

CREATE TABLE IF NOT EXISTS meters (
    meter_id TEXT PRIMARY KEY,
    feeder_id TEXT NOT NULL,
    customer_type TEXT NOT NULL,
    installed_on DATE,
    tariff_band TEXT NOT NULL,
    monthly_kwh_avg NUMERIC(12, 2) CHECK (monthly_kwh_avg >= 0),
    prepaid BOOLEAN NOT NULL,
    CONSTRAINT fk_meters_feeder
        FOREIGN KEY (feeder_id)
        REFERENCES feeders (feeder_id)
);

CREATE TABLE IF NOT EXISTS outages (
    outage_id TEXT PRIMARY KEY,
    feeder_id TEXT NOT NULL,
    start_ts TIMESTAMPTZ NOT NULL,
    end_ts TIMESTAMPTZ NOT NULL,
    duration_min NUMERIC(12, 2) NOT NULL CHECK (duration_min >= 0),
    cause TEXT NOT NULL,
    crew_id TEXT,
    customers_affected INTEGER NOT NULL CHECK (
        customers_affected >= 0
    ),
    CONSTRAINT fk_outages_feeder
        FOREIGN KEY (feeder_id)
        REFERENCES feeders (feeder_id),
    CONSTRAINT chk_outage_time
        CHECK (end_ts >= start_ts)
);

CREATE TABLE IF NOT EXISTS weather (
    feeder_id TEXT NOT NULL,
    weather_date DATE NOT NULL,
    precipitation_sum NUMERIC(10, 2),
    wind_speed_10m_max NUMERIC(10, 2),
    temperature_2m_max NUMERIC(10, 2),
    PRIMARY KEY (feeder_id, weather_date),
    CONSTRAINT fk_weather_feeder
        FOREIGN KEY (feeder_id)
        REFERENCES feeders (feeder_id),
    CONSTRAINT chk_precipitation
        CHECK (
            precipitation_sum IS NULL
            OR precipitation_sum >= 0
        ),
    CONSTRAINT chk_wind_speed
        CHECK (
            wind_speed_10m_max IS NULL
            OR wind_speed_10m_max >= 0
        )
);