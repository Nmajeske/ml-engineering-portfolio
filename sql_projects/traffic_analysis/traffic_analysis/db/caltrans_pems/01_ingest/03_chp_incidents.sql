DELETE FROM raw.chp_incident_day;
-- DuckDB-specific ingestion layer
-- Uses read_csv to load gzipped PEMS files
INSERT INTO raw.chp_incident_day
    SELECT *
    FROM read_csv(
        '{{path}}',
        delim=',',
        header=false,
        timestampformat='%m/%d/%Y %H:%M:%S',
        strict_mode = false, -- tolerate non-conforming rows (resolves error from d03\all_text_chp_incident_day_2025_02_13.txt.gz)
        ignore_errors = true, -- skip bad rows rather than fail
        null_padding = true -- pad out rows that might be missing columns
    )