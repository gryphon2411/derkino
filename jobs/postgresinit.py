import csv
import os
import sys
import time
from pathlib import Path
from uuid import uuid4

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from commons import transform_csv_row_data, create_data_dir, download_archive, extract_csv_from_archive, delete_data_dir
from log import get_logger

logger = get_logger(Path(__file__).stem)
Base = declarative_base()


class TitleBasics(Base):
    __tablename__ = 'title_basics'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tconst = Column(String)
    titleType = Column(String)
    primaryTitle = Column(String)
    originalTitle = Column(String)
    isAdult = Column(Boolean)
    startYear = Column(Integer)
    endYear = Column(Integer)
    runtimeMinutes = Column(Integer)
    genres = Column(ARRAY(String))


def read_csv_data_and_insert_to_database(csv_file_path):
    connection_uri = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
        username=os.getenv('POSTGRES_USERNAME'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),  # 'postgres.postgres-system',
        port=os.getenv('POSTGRES_PORT'),  # 5432,
        database=os.getenv('POSTGRES_DB')
    )
    engine = create_engine(connection_uri)
    session_class = sessionmaker(bind=engine)
    session = session_class()
    write_command_batch_limit_size = 100000
    total_inserted_ids = 0
    total_rows_read = 0
    csv_data = []
    csv_data_size = 0
    csv_data_read_counter = 0

    logger.info(f"Reading {csv_file_path.name} and inserting in bulk to 'title_basics' table at {connection_uri} ...")
    with csv_file_path.open('r', newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')

        for row in reader:
            if csv_data_read_counter >= write_command_batch_limit_size:
                total_inserted_ids += insert_csv_data_to_database(csv_data, session)
                csv_data_read_counter = 0

            transform_csv_row_data(row)

            csv_data.append(row)
            csv_data_size += sys.getsizeof(row)
            total_rows_read += 1
            csv_data_read_counter += 1

        total_inserted_ids += insert_csv_data_to_database(csv_data, session)

    session.commit()
    session.close()

    logger.info(f"Read {total_rows_read:,} csv rows (data size {csv_data_size / 1000 / 1000 / 1000:.3f} gb).")
    logger.info(f'Inserted {total_inserted_ids:,} rows.')


def insert_csv_data_to_database(csv_data, session):
    session.bulk_insert_mappings(TitleBasics, csv_data)
    total_inserted_ids = len(csv_data)
    csv_data.clear()

    return total_inserted_ids


def main():
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

    logger.info(
        f"Done. took {execution_minutes:0.0f}m {execution_seconds:0.0f}s "
        f"({process_minutes:0.0f}m {process_seconds:0.0f}s processing)")


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Job failed.")
        exit(1)
