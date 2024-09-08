import os
import time
import uuid
from pathlib import Path
from typing import Type

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ARRAY, text, Engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from commons import create_data_dir, download_archive, extract_csv_from_archive, \
    delete_data_dir, preprocess_dataframe
from log import get_logger

CONNECTION_URI_TEMPLATE = "postgresql+psycopg2://{username}:{password}@{host}/{database}"

logger = get_logger(Path(__file__).stem)
Base = declarative_base()


class Title(Base):
    __tablename__ = 'title'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tconst = Column(String)
    titleType = Column(String)
    primaryTitle = Column(String)
    originalTitle = Column(String)
    isAdult = Column(Boolean, nullable=True)
    startYear = Column(Integer, nullable=True)
    endYear = Column(Integer, nullable=True)
    runtimeMinutes = Column(Integer, nullable=True)
    genres = Column(ARRAY(String))


def read_csv_data_and_insert_to_database(csv_file_path: Path):
    connection_uri = CONNECTION_URI_TEMPLATE.format(username=os.getenv('POSTGRES_USERNAME'),
                                                    password=os.getenv('POSTGRES_PASSWORD'),
                                                    host=os.getenv('POSTGRES_HOST'),
                                                    database=os.getenv('POSTGRES_DB'))

    engine = create_engine(connection_uri)
    Base.metadata.create_all(engine)  # Creates the table in the database

    preprocessed_csv_file_path = preprocess_title_basic_csv(csv_file_path)
    insert_csv_to_database(engine, preprocessed_csv_file_path, Title)


def preprocess_title_basic_csv(csv_file_path):
    logger.info(f"Reading and preprocessing {csv_file_path.name} ...")

    preprocessed_csv_file_path = csv_file_path.with_name(csv_file_path.stem + '_preprocessed.csv')
    df = pd.read_csv(csv_file_path, delimiter='\t', na_values='\\N', dtype=str)
    preprocess_dataframe(df)
    df.to_csv(preprocessed_csv_file_path, index=False)

    return preprocessed_csv_file_path


def insert_csv_to_database(engine: Engine, preprocessed_csv_file_path: Path, table: Type[Base]):
    logger.info(f"Copying {preprocessed_csv_file_path.name} into '{table.__tablename__}' table at {engine.url} ...")
    connection = engine.raw_connection()
    try:
        with connection.cursor() as cursor:
            with preprocessed_csv_file_path.open("r") as csv_file:
                cursor.copy_expert(f"COPY {table.__tablename__} FROM STDIN WITH CSV HEADER", csv_file)

        connection.commit()
    finally:
        connection.close()

    storage_data_size = preprocessed_csv_file_path.stat().st_size
    total_copied_rows = 0

    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT COUNT(*) FROM {table.__tablename__}"))
        total_copied_rows = result.scalar()

    logger.info(f'Copied {total_copied_rows:,} rows ({storage_data_size / 1000 / 1000 / 1000:.3f} gb).')


def main():
    execution_start, process_start = time.perf_counter(), time.process_time()

    data_dir = create_data_dir()
    archive_file_path = data_dir / 'title.basics.tsv.gz'
    csv_file_path = data_dir / 'data.csv'

    download_archive(archive_file_path)
    extract_csv_from_archive(archive_file_path, csv_file_path)
    read_csv_data_and_insert_to_database(csv_file_path)
    delete_data_dir(data_dir)

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
