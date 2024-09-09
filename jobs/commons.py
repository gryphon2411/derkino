import gzip
import shutil
import uuid
from pathlib import Path

import pandas as pd
import requests
from pandas import DataFrame
from typing_extensions import Optional

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

def preprocess_dataframe(df: DataFrame):
    df['isAdult'] = df['isAdult'].apply(transform_is_adult_cell_data).astype('boolean')
    df['runtimeMinutes'] = pd.to_numeric(df['runtimeMinutes'], downcast='integer', errors='coerce')
    df['startYear'] = pd.to_numeric(df['startYear'], downcast='integer', errors='coerce')
    df['endYear'] = pd.to_numeric(df['endYear'], downcast='integer', errors='coerce')

    # Fills missing startYear and endYear
    df['startYear'] = df['startYear'].fillna(df['endYear'])
    df['endYear'] = df['endYear'].fillna(df['startYear'])

    df['runtimeMinutes'] = df['runtimeMinutes'].astype('Int16')
    df['startYear'] = df['startYear'].astype('Int16')
    df['endYear'] = df['endYear'].astype('Int16')

    # Adds UUIDs
    df['id'] = [str(uuid.uuid4()) for row_index in range(len(df))]

    # Moves 'id' column to be first
    id_column = df.pop('id')
    df.insert(0, 'id', id_column)


def transform_is_adult_cell_data(is_adult_cell_data: Optional[str]):
    if is_adult_cell_data is not None:
        return True if is_adult_cell_data == "1" else False


def delete_data_dir(data_dir):
    shutil.rmtree(data_dir)

    logger.info(f"Deleted {data_dir.absolute()} directory.")


def create_data_dir():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    logger.info(f"Created {data_dir.absolute()} directory.")

    return data_dir
