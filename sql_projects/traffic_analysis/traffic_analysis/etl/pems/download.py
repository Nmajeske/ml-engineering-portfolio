from ._vendor.caltrans_pems.pems.handler import PeMSHandler


def download_files(
    start_year: int,
    end_year: int,
    districts: list[str],
    file_types: list[str],
    months: list[str],
    save_path: str,
) -> PeMSHandler:
    handler = PeMSHandler(username="sebi.goodfellow@utoronto.ca", password="xG*apple3f")
    handler.download_files(
        start_year, end_year, districts, file_types, months, save_path, 0
    )
    return handler
