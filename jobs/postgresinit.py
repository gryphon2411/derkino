import os
import time
import uuid
from pathlib import Path
from typing import Type, Optional

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, text, Engine, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

from commons import create_data_dir, download_archive, extract_csv_from_archive, \
    delete_data_dir, preprocess_dataframe
from log import get_logger

CONNECTION_URI_TEMPLATE = "postgresql+psycopg2://{username}:{password}@{host}/{database}"

logger = get_logger(Path(__file__).stem)
data_dir = None  # type: Optional[Path]
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
    genres = relationship("Genre", secondary="title_genre", back_populates="titles")


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String, unique=True, nullable=False)
    titles = relationship("Title", secondary="title_genre", back_populates="genres")


class TitleGenre(Base):
    __tablename__ = 'title_genre'
    title_id = Column(UUID(as_uuid=True), ForeignKey('title.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genre.id'), primary_key=True)


def read_csv_data_and_insert_to_database(csv_file_path: Path):
    connection_uri = CONNECTION_URI_TEMPLATE.format(username=os.getenv('POSTGRES_USERNAME'),
                                                    password=os.getenv('POSTGRES_PASSWORD'),
                                                    host=os.getenv('POSTGRES_HOST'),
                                                    database=os.getenv('POSTGRES_DB'))

    engine = create_engine(connection_uri)
    Base.metadata.create_all(engine)  # Creates the tables in the database

    preprocessed_df = preprocess_title_basic_csv(csv_file_path)

    process_title_data(engine, preprocessed_df)

    genre_df = process_genre_data(engine, preprocessed_df)
    process_title_genre_data(engine, preprocessed_df, genre_df)


def preprocess_title_basic_csv(csv_file_path: Path):
    logger.info(f"Reading and preprocessing {csv_file_path.name} ...")

    df = pd.read_csv(csv_file_path, delimiter='\t', na_values='\\N', dtype=str)
    preprocess_dataframe(df)

    return df


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


def process_title_data(engine: Engine, preprocessed_df: pd.DataFrame):
    title_csv_path = data_dir / 'title.csv'
    logger.info(f"Processing {title_csv_path.name} ...")

    title_df = generate_title_dataframe(preprocessed_df)
    title_df.to_csv(title_csv_path, index=False)

    insert_csv_to_database(engine, title_csv_path, Title)


def generate_title_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop('genres', axis=1)


def process_genre_data(engine: Engine, preprocessed_df: pd.DataFrame):
    genre_csv_path = data_dir / 'genre.csv'
    logger.info(f"Processing {genre_csv_path.name} ...")

    genre_df = generate_genre_dataframe(preprocessed_df)
    genre_df.to_csv(genre_csv_path, index=False)

    insert_csv_to_database(engine, genre_csv_path, Genre)

    return genre_df


def process_title_genre_data(engine: Engine, preprocessed_df: pd.DataFrame, genre_df: pd.DataFrame):
    title_genre_csv_path = data_dir / 'title_genre.csv'
    logger.info(f"Processing {title_genre_csv_path.name} ...")

    title_genre_df = generate_title_genre_dataframe(preprocessed_df, genre_df)
    title_genre_df.to_csv(title_genre_csv_path, index=False)

    insert_csv_to_database(engine, title_genre_csv_path, TitleGenre)


def generate_genre_dataframe(preprocessed_df: pd.DataFrame) -> pd.DataFrame:
    all_genres = set()

    for index, row in preprocessed_df.iterrows():
        genres = row['genres'].split(',') if isinstance(row['genres'], str) else []
        for genre in genres:
            all_genres.add(genre.strip())
    genre_df = pd.DataFrame({'genre_name': list(all_genres)})
    genre_df.index.name = 'id'

    return genre_df.reset_index()


def generate_title_genre_dataframe(preprocessed_df: pd.DataFrame, genre_df: pd.DataFrame) -> pd.DataFrame:
    genre_dict = dict(zip(genre_df['genre_name'], genre_df['id']))

    title_genre_data = []
    for index, row in preprocessed_df.iterrows():
        if isinstance(row['genres'], str):
            genres = row['genres'].split(',')
            for genre in genres:
                genre_id = genre_dict.get(genre.strip())
                title_genre_data.append({'title_id': row['id'], 'genre_id': genre_id})

    return pd.DataFrame(title_genre_data)


def main():
    global data_dir
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
