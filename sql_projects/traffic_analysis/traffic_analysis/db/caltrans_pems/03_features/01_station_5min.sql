CREATE OR REPLACE TABLE feature.station_5min AS
SELECT
    *,
    EXTRACT(hour FROM timestamp) AS hour,
    EXTRACT(dow FROM timestamp) AS dow,
    EXTRACT(day FROM timestamp) - 1 AS dom,
    EXTRACT(month FROM timestamp ) - 1 AS moy,
    CASE WHEN EXTRACT("dow" FROM timestamp) IN (0,6) THEN TRUE ELSE FALSE END AS is_weekend
FROM clean.station_5min
ORDER BY station, timestamp;

-- NOTE: If we want to create this table to contain only the temporal features to avoid duplication across sensors
--
--CREATE OR REPLACE TABLE temporal_features AS
--SELECT
--    timestamp,
--    EXTRACT(hour FROM timestamp) AS hour,
--    EXTRACT(dow FROM timestamp) AS dow,
--    EXTRACT(day FROM timestamp) - 1 AS dom,
--    EXTRACT(month FROM timestamp ) - 1 AS moy,
--    CASE WHEN EXTRACT("dow" FROM timestamp) IN (0,6) THEN TRUE ELSE FALSE END AS is_weekend
--FROM (
--    SELECT DISTINCT timestamp
--    FROM station_5min_clean
--)
--ORDER BY timestamp;