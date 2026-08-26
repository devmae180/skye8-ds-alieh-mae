-- 1. Total feeders
SELECT COUNT(*) AS total_feeders
FROM feeders;

-- 2. Feeders by town
SELECT tiown, COUNT(*) AS feeder_count
FROM feeders
GROUP BY tiown
ORDER BY feeder_count DESC;

-- 3. Average voltage
SELECT AVG(voltage_kv) AS average_voltage_kv
FROM feeders;

-- 4. Total customers served
SELECT SUM(customers_served) AS total_customers
FROM feeders;

-- 5. Total outages
SELECT COUNT(*) AS total_outages
FROM outages;

-- 6. Outages by feeder
SELECT feeder_id, COUNT(*) AS outage_count
FROM outages
GROUP BY feeder_id
ORDER BY outage_count DESC
LIMIT 10;

-- 7. Total outage duration
SELECT SUM(duration_min) AS total_outage_minutes
FROM outages;

-- 8. Average outage duration
SELECT AVG(duration_min) AS average_outage_minutes
FROM outages;

-- 9. Longest outages
SELECT
    outage_id,
    feeder_id,
    duration_min
FROM outages
ORDER BY duration_min DESC
LIMIT 10;

-- 10. Most affected feeders
SELECT
    f.feeder_id,
    f.tiown,
    COUNT(o.outage_id) AS outage_count
FROM feeders f
JOIN outages o
    ON f.feeder_id = o.feeder_id
GROUP BY f.feeder_id, f.tiown
ORDER BY outage_count DESC
LIMIT 10;

-- 11. Customers by town
SELECT
    tiown,
    SUM(customers_served) AS total_customers
FROM feeders
GROUP BY tiown
ORDER BY total_customers DESC;

-- 12. Meter count by customer type
SELECT
    customer_type,
    COUNT(*) AS meter_count
FROM meters
GROUP BY customer_type
ORDER BY meter_count DESC;

-- 13. Prepaid vs non-prepaid meters
SELECT
    prepaid,
    COUNT(*) AS meter_count
FROM meters
GROUP BY prepaid;

-- 14. Average monthly energy use by customer type
SELECT
    customer_type,
    AVG(monthly_kwh_Avg) AS average_monthly_kwh
FROM meters
GROUP BY customer_type
ORDER BY average_monthly_kwh DESC;

-- 15. Outage count by town
SELECT
    f.tiown,
    COUNT(o.outage_id) AS outage_count
FROM feeders f
JOIN outages o
    ON f.feeder_id = o.feeder_id
GROUP BY f.tiown
ORDER BY outage_count DESC;