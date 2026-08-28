-- 1. Monthly outage minutes per feeder.
SELECT
    feeder_id,
    DATE_TRUNC('month', start_ts)::date AS outage_month,
    SUM(duration_min) AS total_outage_minutes
FROM outages
GROUP BY feeder_id, DATE_TRUNC('month', start_ts)
ORDER BY feeder_id, outage_month;


-- 2. SAIDI and SAIFI per substation per month.
SELECT
    f.substation,
    DATE_TRUNC('month', o.start_ts)::date AS outage_month,
    SUM(o.duration_min * o.customers_affected)
        / NULLIF(SUM(f.customers_served), 0) AS saidi,
    SUM(o.customers_affected)::numeric
        / NULLIF(SUM(f.customers_served), 0) AS saifi
FROM outages AS o
JOIN feeders AS f
    ON o.feeder_id = f.feeder_id
GROUP BY f.substation, DATE_TRUNC('month', o.start_ts)
ORDER BY f.substation, outage_month;


-- 3. Top three feeders by customer-minutes lost within each substation.
WITH feeder_losses AS (
    SELECT
        f.substation,
        o.feeder_id,
        SUM(o.duration_min * o.customers_affected) AS customer_minutes_lost
    FROM outages AS o
    JOIN feeders AS f
        ON o.feeder_id = f.feeder_id
    GROUP BY f.substation, o.feeder_id
),
ranked_losses AS (
    SELECT
        substation,
        feeder_id,
        customer_minutes_lost,
        ROW_NUMBER() OVER (
            PARTITION BY substation
            ORDER BY customer_minutes_lost DESC
        ) AS feeder_rank
    FROM feeder_losses
)
SELECT
    substation,
    feeder_id,
    customer_minutes_lost,
    feeder_rank
FROM ranked_losses
WHERE feeder_rank <= 3
ORDER BY substation, feeder_rank;


-- 4. Seven-day moving average of daily outage count.
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


-- 5A. Nested-subquery version.
SELECT *
FROM (
    SELECT
        feeder_id,
        total_outage_minutes
    FROM (
        SELECT
            feeder_id,
            SUM(duration_min) AS total_outage_minutes
        FROM outages
        GROUP BY feeder_id
    ) AS feeder_totals
    WHERE total_outage_minutes > (
        SELECT AVG(total_outage_minutes)
        FROM (
            SELECT
                feeder_id,
                SUM(duration_min) AS total_outage_minutes
            FROM outages
            GROUP BY feeder_id
        ) AS all_feeder_totals
    )
) AS above_average_feeders
ORDER BY total_outage_minutes DESC;


-- 5B. The same logic rewritten as a chain of CTEs.
WITH feeder_totals AS (
    SELECT
        feeder_id,
        SUM(duration_min) AS total_outage_minutes
    FROM outages
    GROUP BY feeder_id
),
average_total AS (
    SELECT
        AVG(total_outage_minutes) AS average_outage_minutes
    FROM feeder_totals
)
SELECT
    ft.feeder_id,
    ft.total_outage_minutes
FROM feeder_totals AS ft
CROSS JOIN average_total AS a
WHERE ft.total_outage_minutes > a.average_outage_minutes
ORDER BY ft.total_outage_minutes DESC;


-- Weather analysis 1: rainfall and daily outage count.
WITH daily_outages AS (
    SELECT
        feeder_id,
        DATE(start_ts) AS outage_date,
        COUNT(*) AS outage_count
    FROM outages
    GROUP BY feeder_id, DATE(start_ts)
)
SELECT
    CORR(
        w.precipitation_sum,
        COALESCE(d.outage_count, 0)
    ) AS rainfall_outage_count_correlation
FROM weather AS w
LEFT JOIN daily_outages AS d
    ON w.feeder_id = d.feeder_id
    AND w.weather_date = d.outage_date;


-- Weather analysis 2: rainfall and mean outage duration.
WITH daily_outages AS (
    SELECT
        feeder_id,
        DATE(start_ts) AS outage_date,
        AVG(duration_min) AS mean_outage_duration
    FROM outages
    GROUP BY feeder_id, DATE(start_ts)
)
SELECT
    CORR(
        w.precipitation_sum,
        d.mean_outage_duration
    ) AS rainfall_mean_duration_correlation
FROM weather AS w
JOIN daily_outages AS d
    ON w.feeder_id = d.feeder_id
    AND w.weather_date = d.outage_date;


-- Weather analysis 3: rainfall relationship by outage cause.
-- Weather analysis 3: rainfall relationship by outage cause.
-- Correlation between daily rainfall and daily outage count for each cause.

WITH causes AS (

    SELECT DISTINCT cause
    FROM outages
    WHERE cause IS NOT NULL

),

daily_cause_outages AS (

    SELECT

        feeder_id,

        DATE(start_ts) AS outage_date,

        cause,

        COUNT(*) AS outage_count,

        AVG(duration_min) AS mean_outage_duration

    FROM outages

    GROUP BY
        feeder_id,
        DATE(start_ts),
        cause

),

weather_by_cause AS (

    SELECT

        w.feeder_id,

        w.weather_date,

        c.cause,

        w.precipitation_sum,

        COALESCE(d.outage_count, 0) AS outage_count,

        d.mean_outage_duration

    FROM weather AS w

    CROSS JOIN causes AS c

    LEFT JOIN daily_cause_outages AS d

        ON w.feeder_id = d.feeder_id

        AND w.weather_date = d.outage_date

        AND c.cause = d.cause

)

SELECT

    cause,

    CORR(
        precipitation_sum,
        outage_count
    ) AS rainfall_outage_count_correlation,

    CORR(
        precipitation_sum,
        mean_outage_duration
    ) AS rainfall_mean_duration_correlation,

    COUNT(*) FILTER (
        WHERE outage_count > 0
    ) AS days_with_outages

FROM weather_by_cause

GROUP BY cause

ORDER BY rainfall_outage_count_correlation DESC NULLS LAST;