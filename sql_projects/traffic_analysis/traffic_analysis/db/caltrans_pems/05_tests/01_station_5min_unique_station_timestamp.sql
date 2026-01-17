SELECT
    station,
    timestamp,
    COUNT(*) AS row_count
FROM clean.station_5min
GROUP BY station, timestamp
HAVING COUNT(*) > 1;