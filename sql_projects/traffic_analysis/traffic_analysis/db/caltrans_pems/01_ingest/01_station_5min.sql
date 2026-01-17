DELETE FROM raw.station_5min;
-- DuckDB-specific ingestion layer
-- Uses read_csv to load gzipped PEMS files
INSERT INTO raw.station_5min
    SELECT *
    FROM read_csv(
        '{{path}}',
        delim=',',
        header=false,
        columns={{columns}},
        timestampformat='%m/%d/%Y %H:%M:%S'
    )