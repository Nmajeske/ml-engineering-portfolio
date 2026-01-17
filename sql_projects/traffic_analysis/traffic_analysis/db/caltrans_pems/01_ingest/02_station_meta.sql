DELETE FROM raw.station_meta;
-- DuckDB-specific ingestion layer
-- Uses read_csv to load gzipped PEMS files
INSERT INTO raw.station_meta
    SELECT *
    FROM read_csv(
        '{{path}}',
        delim='\t'
    )