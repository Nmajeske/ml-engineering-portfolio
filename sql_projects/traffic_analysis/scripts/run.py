import gzip
import os
import glob

import pandas as pd
import duckdb


def pems_to_db(dir: str, district: str):
    columns = {
        "timestamp": "DATE", # The format is MM/DD/YYYY HH24:MI:SS
        "station": "BIGINT", # Unique station identifier. Use this value to cross-reference with Metadata files.
        "district": "BIGINT", # District #
        "freeway": "BIGINT", # Freeway #
        "direction": "VARCHAR", # N | S | E | W
        "lane_type": "VARCHAR", # A string indicating the type of lane. Possible values (and their meaning are:
                                # CD (Coll/Dist)
                                # CH (Conventional Highway)
                                # FF (Fwy-Fwy connector)
                                # FR (Off Ramp)
                                # HV (HOV)
                                # ML (Mainline)
                                # OR (On Ramp)
        "length": "DOUBLE", # Segment length covered by the station in miles/km.
        "samples": "BIGINT", # Total number of samples received for all lanes.
        "pct_observed": "BIGINT", # Percentage of individual lane points at this location that were observed (e.g. not imputed).
        "total_flow": "BIGINT", # Sum of flows over the 5-minute period across all lanes. Note that the basic 5-minute rollup normalizes flow by the number of good samples received from the controller.
        "avg_occupancy": "DOUBLE", # Average occupancy across all lanes over the 5-minute period expressed as a decimal number between 0 and 1.
        "avg_speed": "DOUBLE", # Flow-weighted average speed over the 5-minute period across all lanes. If flow is 0, mathematical average of 5-minute station speeds.
        "lane1_samples": "BIGINT", # Number of good samples received for lane N. N ranges from 1 to the number of lanes at the location.
        "lane1_flow": "BIGINT", # Total flow for lane N over the 5-minute period normalized by the number of good samples.
        "lane1_avg_occupancy": "BIGINT", # Average occupancy for lane N expressed as a decimal number between 0 and 1. N ranges from 1 to the number of lanes at the location.
        "lane1_avg_speed": "DOUBLE", # 	Flow-weighted average of lane N speeds. If flow is 0, mathematical average of 5-minute lane speeds. N ranges from 1 to the number of lanes
        "lane1_observed": "BOOLEAN", # 1 indicates observed data, 0 indicates imputed.
        "lane2_samples": "BIGINT",
        "lane2_flow": "BIGINT",
        "lane2_avg_occupancy": "BIGINT",
        "lane2_avg_speed": "DOUBLE",
        "lane2_observed": "BOOLEAN",
        "lane3_samples": "BIGINT",
        "lane3_flow": "BIGINT",
        "lane3_avg_occupancy": "BIGINT",
        "lane3_avg_speed": "DOUBLE",
        "lane3_observed": "BOOLEAN",
        "lane4_samples": "BIGINT",
        "lane4_flow": "BIGINT",
        "lane4_avg_occupancy": "BIGINT",
        "lane4_avg_speed": "DOUBLE",
        "lane4_observed": "BOOLEAN",
        "lane5_samples": "BIGINT",
        "lane5_flow": "BIGINT",
        "lane5_avg_occupancy": "BIGINT",
        "lane5_avg_speed": "DOUBLE",
        "lane5_observed": "BOOLEAN",
        "lane6_samples": "BIGINT",
        "lane6_flow": "BIGINT",
        "lane6_avg_occupancy": "BIGINT",
        "lane6_avg_speed": "DOUBLE",
        "lane6_observed": "BOOLEAN",
        "lane7_samples": "BIGINT",
        "lane7_flow": "BIGINT",
        "lane7_avg_occupancy": "BIGINT",
        "lane7_avg_speed": "DOUBLE",
        "lane7_observed": "BOOLEAN",
        "lane8_samples": "BIGINT",
        "lane8_flow": "BIGINT",
        "lane8_avg_occupancy": "BIGINT",
        "lane8_avg_speed": "DOUBLE",
        "lane8_observed": "BOOLEAN",
    }
    db_path = os.path.join(dir, district+'.duckdb')
    conn = duckdb.connect(db_path)
    path = os.path.join(dir, '*.gz')
    query = f"""
    CREATE OR REPLACE TABLE {district} AS
    SELECT *
    FROM read_csv(
        '{path}',
        delim=',',
        header=False,
        columns=?,
        dateformat='%m/%d/%Y %H:%M:%S'
    )
    ORDER BY timestamp
    """
    conn.execute(query, [columns])
    conn.close()
    return db_path
    

if __name__ == "__main__":
    district = 'd03'
    dir = os.path.join('..', 'data', 'caltrans_pems', district)
#    conn = pems_to_db(dir, district)
    print("Hello World!")