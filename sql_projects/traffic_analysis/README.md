# Traffic Analysis for CalTrans PeMS
This project aims to ingest and analyze traffic data from California's Department of Transportation (CalTrans) Performance Measurement System (PeMS).

## Getting Started
To get started, users can install via a local virtual environment or Docker.
### Install
#### Local Python Virtual Environment
```bash
python -m venv .venv
.venv/bin/activate # or .venv\Scripts\activate for Windows
python -m pip install --upgrade pip
pip install -e . # or pip install .[dev]
```
#### Docker
```bash
docker build -t traffic_analysis . # make sure docker is running first if using Windows (e.g. Docker Desktop)
```

### Run the Pipeline
To run the pipeline, users will need to activate their environment (or call the python binary directly) and then invoke the desired stage. 
```bash
# Activate Virtual Environment
.venv/bin/activate # or .venv\Scripts\activate for Windows

# Usage: python -m traffic_analysis <stage> --district <N> [additional args per stage...]
#   Run "python -m traffic_analysis --help" for details

# Download stage:
python -m traffic_analysis download --district 3 --start_year 2025 --end_year 2025 --months January February March
# Extract stage:
python -m traffic_analysis extract --district 3
# Build stage:
python -m traffic_analysis build --district 3
# Analyze stage:
python -m traffic_analysis analyze --district 3
# Test stage:
python -m traffic_analysis test --district 3
```

## Core Pipeline
The entrypoint for this project can be found at traffic_analysis/__main__.py in which all major stages of the pipeline are orchestrated. Databases are generally constructed by the stages:

download -> extract -> build

The following downloads Jan-Mar of 2025 for district 3, extracts raw files, and builds a database:
```bash
python -m traffic_analysis download --district 3 --start_year 2025 --end_year 2025 --months January February March
python -m traffic_analysis extract --district 3
python -m traffic_analysis build --district 3
# saved at ../../data/processed/caltrans_pems/d03/d03.duckdb
```

Once built, uses can execute various database analyses:
```bash
python -m traffic_analysis analyze --district 3
# see traffic_analysis/db/caltrans_pems/04_analytics/ for more
```

Several tests are available to validate the curated database:
```bash
python -m traffic_analysis test --district 3
# see traffic_analysis/db/caltrans_pems/05_tests/ for more
```

## Vendored Functionalities
This project utilizes various third-party tools/applications, including:
1. CalTrans PEMS by Sebastian D. Goodfellow @ https://github.com/Seb-Good/caltrans-pems
    - Functionality: download data from CalTrans PeMS' data clearing house @ https://pems.dot.ca.gov/.
    - Location: [./traffic_analysis/etl/pems/_vendor/caltrans_pems](./traffic_analysis/etl/pems/_vendor/caltrans_pems)