from pathlib import Path

import duckdb
from jinja2 import Template


def run_sql(conn: duckdb.DuckDBPyConnection, sql_path: Path, **kwargs: dict) -> duckdb.DuckDBPyConnection:
    sql = sql_path.read_text()
    sql = Template(sql).render(**kwargs)
    return conn.execute(sql)
