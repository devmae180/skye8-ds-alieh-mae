-- 1. Monthly outage minutes per feeder
SELECT
    feeder_id,
    DATE_TRUNC('month', start_ts) AS month,
    SUM(duration_min) AS total_outage_minutes
FROM outages
GROUP BY feeder_id, DATE_TRUNC('month', start_ts)
ORDER BY month, feeder_id;


-- 2. SAIDI and SAIFI per substation per month
SELECT
    f.substation,
    DATE_TRUNC('month', o.start_ts) AS month,
    SUM(o.duration_min * o.customers_affected)
        / NULLIF(SUM(f.customers_served), 0) AS saidi,
    COUNT(o.outage_id)::NUMERIC
        / NULLIF(SUM(f.customers_served), 0) AS saifi
FROM outages o
JOIN feeders f
    ON o.feeder_id = f.feeder_id
GROUP BY
    f.substation,
    DATE_TRUNC('month', o.start_ts)
ORDER BY month, f.substation;


-- 3. Top three feeders by customer-minutes lost
-- within each substation
WITH feeder_losses AS (
    SELECT
        f.substation,
        o.feeder_id,
        SUM(o.duration_min * o.customers_affected)
            AS customer_minutes_lost
    FROM outages o
    JOIN feeders f
        ON o.feeder_id = f.feeder_id
    GROUP BY f.substation, o.feeder_id
),
ranked AS (
    SELECT
        substation,
        feeder_id,
        customer_minutes_lost,
        ROW_NUMBER() OVER (
            PARTITION BY substation
            ORDER BY customer_minutes_lost DESC
        ) AS rank
    FROM feeder_losses
)
SELECT
    substation,
    feeder_id,
    customer_minutes_lost
FROM ranked
WHERE rank <= 3
ORDER BY substation, rank;


-- 4. Seven-day moving average of daily outage count
WITH daily_outages AS (
    SELECT
        DATE(start_ts) AS outage_date,
        COUNT(*) AS outage_count
    FROM outages
    GROUP BY DATE(start_ts)
)
SELECT
    outage_date,
    outage_count,
    AVG(outage_count) OVER (
        ORDER BY outage_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_day_moving_average
FROM daily_outages
ORDER BY outage_date;


-- 5. Nested subquery rewritten using CTEs
-- Find feeders whose outage count is above the average
-- outage count across all feeders.

WITH feeder_counts AS (
    SELECT
        feeder_id,
        COUNT(*) AS outage_count
    FROM outages
    GROUP BY feeder_id
),
average_count AS (
    SELECT AVG(outage_count) AS avg_outage_count
    FROM feeder_counts
)
SELECT
    feeder_id,
    outage_count
FROM feeder_counts
WHERE outage_count > (
    SELECT avg_outage_count
    FROM average_count
)
ORDER BY outage_count DESC;