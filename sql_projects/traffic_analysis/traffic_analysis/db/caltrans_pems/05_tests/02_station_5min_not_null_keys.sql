SELECT *
FROM clean.station_5min
WHERE station IS NULL OR timestamp IS NULL;