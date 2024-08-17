import gzip
import shutil
from pathlib import Path

import requests

from log import get_logger

logger = get_logger(Path(__file__).stem)


def download_archive(archive_file_path):
    url = f'https://datasets.imdbws.com/{archive_file_path.name}'
    logger.info(f'Downloading {url} into {archive_file_path.parent.absolute()}...')
    logger.info("""\
    Information courtesy of
    IMDb
    (https://www.imdb.com).
    Used with permission.""")
    response = requests.get(url, stream=True)
    with archive_file_path.open('wb') as file:
        shutil.copyfileobj(response.raw, file)

    logger.info(f"Downloaded ({archive_file_path.stat().st_size / 1000 / 1000:.3f} mb).")


def extract_csv_from_archive(archive_file_path, csv_file_path):
    logger.info(f"Extracting {csv_file_path.name} into {archive_file_path.parent.absolute()}...")
    with gzip.open(archive_file_path, 'rb') as file:
        with csv_file_path.open('wb') as csv_file:
            shutil.copyfileobj(file, csv_file)

    logger.info(f"Extracted ({csv_file_path.stat().st_size / 1000 / 1000:.3f} mb).")


def transform_csv_row_data(row):
    try:
        for cell_key, cell_value in row.items():
            if cell_value:
                if "\\N" in cell_value:
                    cell_value = None

                if cell_key == "genres":
                    if cell_value:
                        cell_value = cell_value.split(",") if "," in cell_value else [cell_value]
                    else:
                        cell_value = []

                elif cell_key == "isAdult":
                    if cell_value:
                        cell_value = True if cell_value == "1" else False

                elif cell_key in ["runtimeMinutes", "startYear", "endYear"]:
                    if cell_value:
                        cell_value = int(cell_value) if cell_value.isdigit() else None

                row[cell_key] = cell_value

        if row["endYear"] and not row["startYear"]:
            row["startYear"] = row["endYear"]
        elif row["startYear"] and not row["endYear"]:
            row["endYear"] = row["startYear"]
    except Exception:
        logger.exception(f"Row transform failed: {row}")
        raise


def delete_data_dir(data_dir):
    logger.info(f"Deleting {data_dir.absolute()} directory...")
    shutil.rmtree(data_dir)

    logger.info(f"Deleted.")


def create_data_dir():
    data_dir = Path("data")
    logger.info(f"Creating {data_dir.absolute()} directory...")
    data_dir.mkdir(exist_ok=True)

    return data_dir
