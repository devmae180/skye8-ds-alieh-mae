-- Performance analysis: before adding the index.

EXPLAIN ANALYZE
SELECT *
FROM outages
WHERE feeder_id = 'FD-001'
ORDER BY start_ts;


-- Add an index for feeder-specific outage lookups ordered by time.

CREATE INDEX IF NOT EXISTS idx_outages_feeder_start_ts
ON outages (feeder_id, start_ts);


-- Performance analysis: after adding the index.

EXPLAIN ANALYZE
SELECT *
FROM outages
WHERE feeder_id = 'FD-001'
ORDER BY start_ts;


-- Record the comparison:
-- Before index: copy EXPLAIN ANALYZE output here after running it.
-- After index: copy EXPLAIN ANALYZE output here after running it.
--
-- Explanation:
-- The index allows PostgreSQL to locate rows for a feeder using the
-- indexed feeder_id and retrieve them in start_ts order. Depending on
-- table size and PostgreSQL's cost estimates, the plan may change from
-- a sequential scan plus sort to an index scan.