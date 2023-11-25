import csv
import gzip
import shutil
import sys
from pathlib import Path

import requests
from pymongo import MongoClient

from log import get_logger

logger = get_logger(Path(__file__).stem)


def download_archive(archive_file_path):
    url = f'https://datasets.imdbws.com/{archive_file_path.name}'
    logger.info(f'Downloading {url} into {archive_file_path.parent.absolute()}...')
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


def read_csv(csv_file_path):
    logger.info(f"Reading {csv_file_path.name} ...")
    data = []
    data_size = 0
    with csv_file_path.open('r', newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')

        for row in reader:
            for cell_key, cell_value in row.items():
                if cell_value and "\\N" in cell_value:
                    row[cell_key] = None
            data.append(row)
            data_size += sys.getsizeof(row)

    logger.info(f"Read {len(data):,} lines ({data_size / 1000 / 1000 / 1000:.3f} gb).")
    return data


def delete_data_dir(data_dir):
    logger.info(f"Deleting {data_dir.absolute()} directory...")
    shutil.rmtree(data_dir)

    logger.info(f"Deleted.")


def create_data_dir():
    data_dir = Path("data")
    logger.info(f"Creating {data_dir.absolute()} directory...")
    data_dir.mkdir(exist_ok=True)

    return data_dir


data_dir_ = create_data_dir()

archive_file_path_ = data_dir_ / 'title.basics.tsv.gz'
csv_file_path_ = data_dir_ / 'data.csv'

download_archive(archive_file_path_)
extract_csv_from_archive(archive_file_path_, csv_file_path_)
data_ = read_csv(csv_file_path_)

# Connect to MongoDB
# client = MongoClient(os.getenv('MONGODB_URI'))
# db = client.test

# Insert data into MongoDB
# db.movies.insert_many(data)

delete_data_dir(data_dir_)
