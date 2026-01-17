SELECT *
FROM clean.station_5min
WHERE
    lane1_samples < 0
    OR lane1_flow < 0
    OR lane1_avg_occupancy NOT BETWEEN 0.0 AND 1.0
    OR lane1_avg_speed < 0
    OR lane1_observed NOT IN (0,1);