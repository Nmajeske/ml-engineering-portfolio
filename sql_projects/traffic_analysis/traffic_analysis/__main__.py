import os

from traffic_analysis.etl import pems_to_db
from traffic_analysis.etl.pems.download import download_files


def main():
    district = "d03"
    dir = os.path.join("..", "..", "data", "raw", "caltrans_pems", district)
    print("Hello World!")


#    conn = pems_to_db(dir, district)
#    download_files(2001, 2002, ['3'], ['station_5min'], ['January'], os.path.join("..", "..", "data", "test"))


if __name__ == "__main__":
    main()
