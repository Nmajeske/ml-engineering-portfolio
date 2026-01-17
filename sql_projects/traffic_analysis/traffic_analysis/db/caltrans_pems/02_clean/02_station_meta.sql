CREATE OR REPLACE TABLE clean.station_meta AS
SELECT DISTINCT
    CAST(station AS BIGINT) AS station,
    CAST(freeway AS BIGINT) AS freeway,
    CAST(direction AS VARCHAR) AS direction,
    CAST(district AS BIGINT) AS district,
    CAST(county AS BIGINT) AS county,
    CAST(city AS BIGINT) AS city,
    CAST(state_pm AS VARCHAR) AS state_pm,
    CAST(abs_pm AS VARCHAR) AS abs_pm,
    CAST(latitude AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    CAST(length AS DOUBLE) AS length,
    CAST(lane_type AS VARCHAR) AS lane_type,
    CAST(lanes AS BIGINT) AS lanes,
    CAST(name AS VARCHAR) AS name,
    CAST(user_id_1 AS BIGINT) AS user_id_1,
    CAST(user_id_2 AS BIGINT) AS user_id_2,
    CAST(user_id_3 AS BIGINT) AS user_id_3,
    CAST(user_id_4 AS BIGINT) AS user_id_4
FROM raw.station_meta
WHERE station IS NOT NULL
ORDER BY station;