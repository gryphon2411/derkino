import csv
import gzip
import os
import shutil
import sys
import time
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


def read_csv_data_and_insert_to_database(csv_file_path):
    client = MongoClient(os.getenv('MONGO_URI'))
    client.server_info()  # Blocks until the connection is ready
    db = client.imdb
    write_command_batch_limit_size = 100000  # https://www.mongodb.com/docs/manual/reference/limits/#mongodb-limit-Write-Command-Batch-Limit-Size
    total_inserted_ids = 0
    total_rows_read = 0
    csv_data = []
    csv_data_size = 0
    csv_data_read_counter = 0

    logger.info(f"Reading {csv_file_path.name} and inserting in bulk to '{db.name}' database "
                f"('title_basics' collection) at {client.address} ...")
    with csv_file_path.open('r', newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')

        for row in reader:
            if csv_data_read_counter >= write_command_batch_limit_size:
                total_inserted_ids += insert_csv_data_to_database_2(csv_data, db)
                csv_data_read_counter = 0

            for cell_key, cell_value in row.items():
                if cell_value and "\\N" in cell_value:
                    row[cell_key] = None

            csv_data.append(row)
            csv_data_size += sys.getsizeof(row)
            total_rows_read += 1
            csv_data_read_counter += 1

        total_inserted_ids += insert_csv_data_to_database_2(csv_data, db)

    logger.info(f"Read {total_rows_read:,} csv rows (data size {csv_data_size / 1000 / 1000 / 1000:.3f} gb).")
    logger.info(f'Inserted {total_inserted_ids:,} documents.')


def insert_csv_data_to_database_2(csv_data, db):
    total_inserted_ids = len(db.title_basics.insert_many(csv_data).inserted_ids)
    csv_data.clear()

    return total_inserted_ids


def delete_data_dir(data_dir):
    logger.info(f"Deleting {data_dir.absolute()} directory...")
    shutil.rmtree(data_dir)

    logger.info(f"Deleted.")


def create_data_dir():
    data_dir = Path("data")
    logger.info(f"Creating {data_dir.absolute()} directory...")
    data_dir.mkdir(exist_ok=True)

    return data_dir


execution_start, process_start = time.perf_counter(), time.process_time()

data_dir_ = create_data_dir()

archive_file_path_ = data_dir_ / 'title.basics.tsv.gz'
csv_file_path_ = data_dir_ / 'data.csv'

download_archive(archive_file_path_)
extract_csv_from_archive(archive_file_path_, csv_file_path_)
read_csv_data_and_insert_to_database(csv_file_path_)
delete_data_dir(data_dir_)

execution_end, process_end = time.perf_counter(), time.process_time()
execution_duration = execution_end - execution_start
process_duration = process_end - process_start
execution_minutes, execution_seconds = divmod(execution_duration, 60)
process_minutes, process_seconds = divmod(process_duration, 60)

logger.info(f"Done. took {execution_minutes:0.0f}m {execution_seconds:0.0f}s "
            f"({process_minutes:0.0f}m {process_seconds:0.0f}s processing)")
