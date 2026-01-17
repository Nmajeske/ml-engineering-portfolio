CREATE OR REPLACE VIEW analysis.missing_intervals AS
WITH diffs AS (
    SELECT
        station,
        timestamp,
        LAG(timestamp) OVER (PARTITION BY station ORDER BY timestamp) AS previous_timestamp
    FROM feature.station_5min
)
SELECT
    station,
    COUNT(*) FILTER (WHERE previous_timestamp IS NOT NULL AND timestamp - previous_timestamp > INTERVAL '5 minutes') AS gap_count,
    MAX(timestamp - previous_timestamp) FILTER (WHERE previous_timestamp IS NOT NULL) AS max_gap
FROM diffs
GROUP BY station
ORDER BY gap_count DESC
LIMIT 50;