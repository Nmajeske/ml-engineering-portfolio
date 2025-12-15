import os

from traffic_analysis.etl import pems_to_db


def main():
    district = "d03"
    dir = os.path.join("..", "..", "data", "raw", "caltrans_pems", district)
    #    conn = pems_to_db(dir, district)
    print("Hello World!")


if __name__ == "__main__":
    main()
