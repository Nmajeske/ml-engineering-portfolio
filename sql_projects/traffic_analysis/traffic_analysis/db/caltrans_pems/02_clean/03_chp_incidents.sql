CREATE OR REPLACE TABLE clean.chp_incident_day AS
SELECT DISTINCT
    CAST(incident_id AS BIGINT) AS incident_id,
    CAST(cc_code AS VARCHAR) AS cc_code,
    CAST(incident_num AS BIGINT) AS incident_num,
    CAST(timestamp AS TIMESTAMP) AS timestamp,
    CAST(description AS VARCHAR) AS description,
    CAST(location AS VARCHAR) AS location,
    CAST(area AS VARCHAR) AS area,
    CAST(zoom_map AS VARCHAR) AS zoom_map,
    CAST(tb_xy AS DOUBLE) AS tb_xy,
    CAST(latitude AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    CAST(district AS BIGINT) AS district, -- District #
    CAST(county_fips_id AS BIGINT) AS county_fips_id,
    CAST(city_fips_id AS BIGINT) AS city_fips_id,
    CAST(freeway AS BIGINT) AS freeway,  -- Freeway #
    CAST(direction AS VARCHAR) AS direction,
    CAST(state_pm AS VARCHAR) AS state_pm,
    CAST(abs_pm AS VARCHAR) AS abs_pm,
    CAST(severity AS VARCHAR) AS severity,
    CAST(duration AS BIGINT) AS duration
FROM raw.chp_incident_day
WHERE timestamp IS NOT NULL and incident_id IS NOT NULL
ORDER BY incident_id, timestamp;