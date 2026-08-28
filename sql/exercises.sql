-- SQL Exercises: Grid Reliability Database
-- Questions increase in difficulty from 1 to 25.

-- 1. Show all feeders.
SELECT *
FROM feeders;

-- 2. Show the feeder ID and town for every feeder.
SELECT feeder_id, town
FROM feeders;

-- 3. Find feeders located in Bamenda.
SELECT *
FROM feeders
WHERE town = 'Bamenda';

-- 4. Find feeders serving more than 5,000 customers.
SELECT *
FROM feeders
WHERE customers_served > 5000;

-- 5. Show outages longer than 60 minutes.
SELECT *
FROM outages
WHERE duration_min > 60;

-- 6. Find outages caused by a selected cause.
SELECT *
FROM outages
WHERE cause = 'Weather';

-- 7. Count the total number of outages.
SELECT COUNT(*) AS total_outages
FROM outages;

-- 8. Find the average outage duration.
SELECT AVG(duration_min) AS average_outage_duration
FROM outages;

-- 9. Count the number of feeders in each town.
SELECT town, COUNT(*) AS feeder_count
FROM feeders
GROUP BY town;

-- 10. Find towns with more than two feeders.
SELECT town, COUNT(*) AS feeder_count
FROM feeders
GROUP BY town
HAVING COUNT(*) > 2;

-- 11. Find the total number of outages for each feeder.
SELECT feeder_id, COUNT(*) AS outage_count
FROM outages
GROUP BY feeder_id;

-- 12. Find feeders with more than 50 outages.
SELECT feeder_id, COUNT(*) AS outage_count
FROM outages
GROUP BY feeder_id
HAVING COUNT(*) > 50;

-- 13. INNER JOIN: Show outages with feeder information.
SELECT o.outage_id, f.town, o.duration_min
FROM outages AS o
INNER JOIN feeders AS f
    ON o.feeder_id = f.feeder_id;

-- 14. LEFT JOIN: Show all feeders and any outages.
SELECT f.feeder_id, o.outage_id
FROM feeders AS f
LEFT JOIN outages AS o
    ON f.feeder_id = o.feeder_id;

-- 15. RIGHT JOIN: Show all outages and matching feeders.
SELECT f.feeder_id, o.outage_id
FROM feeders AS f
RIGHT JOIN outages AS o
    ON f.feeder_id = o.feeder_id;

-- 16. FULL OUTER JOIN: Include all feeders and outages.
SELECT f.feeder_id, o.outage_id
FROM feeders AS f
FULL OUTER JOIN outages AS o
    ON f.feeder_id = o.feeder_id;

-- 17. Find feeders above the average number of customers served.
SELECT *
FROM feeders
WHERE customers_served > (
    SELECT AVG(customers_served)
    FROM feeders
);

-- 18. Find outages longer than the average outage duration.
SELECT *
FROM outages
WHERE duration_min > (
    SELECT AVG(duration_min)
    FROM outages
);

-- 19. Find the feeder with the highest average outage duration.
SELECT feeder_id, AVG(duration_min) AS average_duration
FROM outages
GROUP BY feeder_id
ORDER BY average_duration DESC
LIMIT 1;

-- 20. UNION: Feeder IDs found in outages or weather.
SELECT feeder_id FROM outages
UNION
SELECT feeder_id FROM weather;

-- 21. UNION ALL: Combine feeder IDs including duplicates.
SELECT feeder_id FROM outages
UNION ALL
SELECT feeder_id FROM weather;

-- 22. INTERSECT: Feeder IDs found in both tables.
SELECT feeder_id FROM outages
INTERSECT
SELECT feeder_id FROM weather;

-- 23. EXCEPT: Outage feeders not found in weather.
SELECT feeder_id FROM outages
EXCEPT
SELECT feeder_id FROM weather;

-- 24. Show how aggregates handle NULL values.
SELECT
    COUNT(*) AS total_rows,
    COUNT(crew_id) AS non_null_crew_ids,
    AVG(duration_min) AS average_duration,
    SUM(duration_min) AS total_duration
FROM outages;

-- 25. Grouping behaviour when crew_id is NULL.
SELECT
    crew_id,
    COUNT(*) AS outage_count,
    AVG(duration_min) AS average_duration
FROM outages
GROUP BY crew_id
ORDER BY outage_count DESC;