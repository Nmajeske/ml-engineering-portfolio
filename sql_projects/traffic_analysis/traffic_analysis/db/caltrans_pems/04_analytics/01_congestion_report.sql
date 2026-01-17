CREATE OR REPLACE VIEW analysis.congestion_summary AS
SELECT
    station,
    AVG(lane1_avg_speed) AS avg_speed,
    COUNT(*) AS n_samples
FROM feature.station_5min
WHERE is_weekend = False AND hour in (16,17,18)
GROUP BY station
HAVING COUNT(*) > 100
ORDER BY avg_speed
LIMIT 15;