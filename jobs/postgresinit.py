import os
import time
from pathlib import Path
from uuid import uuid4

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, declarative_base

from commons import create_data_dir, download_archive, extract_csv_from_archive, \
    delete_data_dir, preprocess_dataframe
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


def read_csv_data_and_insert_to_database(csv_file_path: Path):
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

    logger.info(f"Reading {csv_file_path.name} into a dataframe...")
    df = pd.read_csv(csv_file_path, delimiter='\t', na_values='\\N')

    logger.info(f"Transforming {csv_file_path.name} dataframe data...")
    preprocess_dataframe(df)

    logger.info(f"Inserting {csv_file_path.name} in bulk to 'title_basics' table at {connection_uri} ...")
    memory_data_size = df.memory_usage(deep=True).sum()
    storage_data_size = csv_file_path.stat().st_size
    df.to_sql('title_basics', engine, if_exists='append', index=False, method='multi', chunksize=100000)

    total_inserted_ids = len(df)

    session.commit()
    session.close()

    logger.info(f'Inserted {total_inserted_ids:,} rows ('
                f'memory: {memory_data_size / 1000 / 1000 / 1000:.3f} gb, '
                f'storage: {storage_data_size / 1000 / 1000 / 1000:.3f} gb).')


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
