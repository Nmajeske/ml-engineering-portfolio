import argparse
import glob
import os
import sys
import zipfile
from pathlib import Path
from typing import Optional

import duckdb
import pandas as pd
from dotenv import load_dotenv

from traffic_analysis.db.pipeline import run_sql
from traffic_analysis.etl.pems.download import download_files

load_dotenv()
columns = {
    "timestamp": "TIMESTAMP",  # The format is MM/DD/YYYY HH24:MI:SS
    "station": "BIGINT",  # Unique station identifier. Use this value to cross-reference with Metadata files.
    "district": "BIGINT",  # District #
    "freeway": "BIGINT",  # Freeway #
    "direction": "VARCHAR",  # N | S | E | W
    "lane_type": "VARCHAR",  # A string indicating the type of lane. Possible values (and their meaning are:
    # CD (Coll/Dist)
    # CH (Conventional Highway)
    # FF (Fwy-Fwy connector)
    # FR (Off Ramp)
    # HV (HOV)
    # ML (Mainline)
    # OR (On Ramp)
    "length": "DOUBLE",  # Segment length covered by the station in miles/km.
    "samples": "BIGINT",  # Total number of samples received for all lanes.
    "pct_observed": "BIGINT",  # Percentage of individual lane points at this location that were observed (e.g. not imputed).
    "total_flow": "BIGINT",  # Sum of flows over the 5-minute period across all lanes. Note that the basic 5-minute rollup normalizes flow by the number of good samples received from the controller.
    "avg_occupancy": "DOUBLE",  # Average occupancy across all lanes over the 5-minute period expressed as a decimal number between 0 and 1.
    "avg_speed": "DOUBLE",  # Flow-weighted average speed over the 5-minute period across all lanes. If flow is 0, mathematical average of 5-minute station speeds.
    "lane1_samples": "BIGINT",  # Number of good samples received for lane N. N ranges from 1 to the number of lanes at the location.
    "lane1_flow": "BIGINT",  # Total flow for lane N over the 5-minute period normalized by the number of good samples.
    "lane1_avg_occupancy": "BIGINT",  # Average occupancy for lane N expressed as a decimal number between 0 and 1. N ranges from 1 to the number of lanes at the location.
    "lane1_avg_speed": "DOUBLE",  # 	Flow-weighted average of lane N speeds. If flow is 0, mathematical average of 5-minute lane speeds. N ranges from 1 to the number of lanes
    "lane1_observed": "BOOLEAN",  # 1 indicates observed data, 0 indicates imputed.
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


def build_parser() -> argparse.ArgumentParser:
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--config", type=str, default=None)
    parent_parser.add_argument("--district", type=int, required=True)
    parent_parser.add_argument("--data_dir", type=str, default=os.path.join("..", "..", "data"))
    parent_parser.add_argument("--sql_dir", type=str, default=os.path.join("traffic_analysis", "db", "caltrans_pems"))
    parent_parser.add_argument("--log-level", type=str, default="INFO")

    parser = argparse.ArgumentParser(prog="traffic_analysis")
    sub = parser.add_subparsers(dest="command", required=True)

    download_parser = sub.add_parser("download", parents=[parent_parser], help="Download raw PeMS data")
    download_parser.add_argument("--start_year", type=int, required=True)
    download_parser.add_argument("--end_year", type=int, required=True)
    download_parser.add_argument(
        "--months",
        type=list[str],
        nargs="+",
        default=["January", "February", "March"],
    )
    download_parser.add_argument(
        "--file_types",
        type=list[str],
        nargs="+",
        default=["station_5min", "meta", "chp_incidents_day"],
    )

    extract_parser = sub.add_parser("extract", parents=[parent_parser], help="Extract downloaded PeMS data")
    extract_parser.add_argument(
        "--file_types",
        type=list[str],
        nargs="+",
        default=["station_5min", "meta", "chp_incidents_day"],
    )

    build_parser = sub.add_parser("build", parents=[parent_parser], help="Build DuckDB database")

    analyze_parser = sub.add_parser("analyze", parents=[parent_parser], help="Run analysis queries")

    test_parser = sub.add_parser("test", parents=[parent_parser], help="Run test queries")

    return parser


def download(args: argparse.Namespace, raw_dir: Path, processed_dir: Path):
    download_files(
        args.start_year,
        args.end_year,
        [args.district],
        args.file_types,
        args.months,
        raw_dir,
        os.getenv("PEMS_USERNAME"),
        os.getenv("PEMS_PASSWORD"),
    )


def extract(args: argparse.Namespace, raw_dir: Path, processed_dir: Path):
    if "chp_incidents_day" in args.file_types:
        paths = sorted(
            glob.glob(
                os.path.join(
                    raw_dir,
                    "all_text_chp_incidents_day_[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9].txt.zip",
                )
            )
        )
        for path in paths:
            print(f"Extracting {path}")
            try:
                with zipfile.ZipFile(path, "r") as f:
                    f.extractall(raw_dir)
                    _path = path.replace("incidents", "incident").replace(".txt.zip", ".txt.gz")
                    df = pd.read_csv(_path)
                    print(f"{_path}.shape =", df.shape)
            except zipfile.BadZipFile as exc:
                print(f"Could not unzip {path}. File may be corrupted or empty.")


def build_db(args: argparse.Namespace, raw_dir: Path, processed_dir: Path):
    district_label = f"d{args.district:02d}"
    db_path = os.path.join(processed_dir, district_label + ".duckdb")
    conn = duckdb.connect(db_path)
    ### Create Tables ###
    sql_path = Path(os.path.join(args.sql_dir, "00_schema", "00_tables.sql"))
    run_sql(conn, sql_path, district=district_label)
    ### Ingest Data ###
    # station time-series
    sql_path = Path(os.path.join(args.sql_dir, "01_ingest", "01_station_5min.sql"))
    path = os.path.join(raw_dir, f"{district_label}_text_station_5min_*.txt.gz")
    run_sql(conn, sql_path, district=district_label, path=path, columns=columns)
    res = conn.sql(f"SELECT * FROM raw.station_5min")
    res.show()
    # station meta
    sql_path = Path(os.path.join(args.sql_dir, "01_ingest", "02_station_meta.sql"))
    path = sorted(glob.glob(os.path.join(raw_dir, "*_meta_*")))[-1]  # take the latest metadata file
    run_sql(conn, sql_path, district=district_label, path=path)
    res = conn.sql(f"SELECT * FROM raw.station_meta")
    res.show()
    # incidents
    sql_path = Path(os.path.join(args.sql_dir, "01_ingest", "03_chp_incidents.sql"))
    path = os.path.join(
        raw_dir,
        "all_text_chp_incident_day_[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9].txt.gz",
    )
    run_sql(conn, sql_path, path=path)
    res = conn.sql(f"SELECT * FROM raw.chp_incident_day")
    res.show()
    ### Clean Tables ###
    # station time-series
    sql_path = Path(os.path.join(args.sql_dir, "02_clean", "01_station_5min.sql"))
    run_sql(conn, sql_path)
    res = conn.sql(f"SELECT * FROM clean.station_5min")
    res.show()
    # station meta
    sql_path = Path(os.path.join(args.sql_dir, "02_clean", "02_station_meta.sql"))
    run_sql(conn, sql_path)
    res = conn.sql(f"SELECT * FROM clean.station_meta")
    res.show()
    # incidents
    sql_path = Path(os.path.join(args.sql_dir, "02_clean", "03_chp_incidents.sql"))
    run_sql(conn, sql_path)
    res = conn.sql(f"SELECT * FROM clean.chp_incident_day")
    res.show()
    ### Create Features ###
    # station time-series features
    sql_path = Path(os.path.join(args.sql_dir, "03_features", "01_station_5min.sql"))
    run_sql(conn, sql_path)
    res = conn.sql(f"SELECT * FROM feature.station_5min")
    res.show()


def analyze_db(args: argparse.Namespace, raw_dir: Path, processed_dir: Path):
    district_label = f"d{args.district:02d}"
    db_path = os.path.join(processed_dir, district_label + ".duckdb")
    conn = duckdb.connect(db_path)
    ### Run Analytics ###
    # station time-series congestion report
    sql_path = Path(os.path.join(args.sql_dir, "04_analytics", "01_congestion_report.sql"))
    run_sql(conn, sql_path)
    res = conn.sql(f"SELECT * FROM analysis.congestion_summary")
    res.show()
    # station time-series data quality report
    sql_path = Path(os.path.join(args.sql_dir, "04_analytics", "02_quality_report.sql"))
    run_sql(conn, sql_path)
    res = conn.sql(f"SELECT * FROM analysis.missing_intervals")
    res.show()


def test_db(args: argparse.Namespace, raw_dir: Path, processed_dir: Path):
    district_label = f"d{args.district:02d}"
    db_path = os.path.join(processed_dir, district_label + ".duckdb")
    conn = duckdb.connect(db_path)
    ### Run Tests ###
    # station time-series uniqueness tests
    sql_path = Path(
        os.path.join(
            args.sql_dir,
            "05_tests",
            "01_station_5min_unique_station_timestamp.sql",
        )
    )
    df = run_sql(conn, sql_path).df()
    assert df.empty, f"Failed tests from {sql_path}"
    # station time-series not null tests
    sql_path = Path(os.path.join(args.sql_dir, "05_tests", "02_station_5min_not_null_keys.sql"))
    df = run_sql(conn, sql_path).df()
    assert df.empty, f"Failed tests from {sql_path}"
    # station time-series value ranges tests
    sql_path = Path(os.path.join(args.sql_dir, "05_tests", "03_station_5min_value_ranges.sql"))
    df = run_sql(conn, sql_path).df()
    assert df.empty, f"Failed tests from {sql_path}"


def main(argv: Optional[list[str]] = None):
    if argv is None:
        argv = sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    district_label = f"d{args.district:02d}"
    raw_dir = os.path.join(args.data_dir, "raw", "caltrans_pems", district_label)
    processed_dir = os.path.join(args.data_dir, "processed", "caltrans_pems", district_label)
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    ### Run Stage ###
    if args.command == "download":
        download(args, raw_dir, processed_dir)
    elif args.command == "extract":
        extract(args, raw_dir, processed_dir)
    elif args.command == "build":
        build_db(args, raw_dir, processed_dir)
    elif args.command == "analyze":
        analyze_db(args, raw_dir, processed_dir)
    elif args.command == "test":
        test_db(args, raw_dir, processed_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
