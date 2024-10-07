from datetime import date
from pathlib import Path

from sqlalchemy import func
from sqlalchemy.orm import Session

from log import get_logger
from postgresinit.schemas import Title, Genre, TitleGenre


logger = get_logger(Path(__file__).stem)


def report_title_data(session: Session):
    logger.info("Running Title report...")

    total_titles = session.query(Title).count()
    logger.info(f"Total titles: {total_titles}")

    null_adult_titles = session.query(Title).filter(Title.isAdult.is_(None)).count()
    logger.info(f"Titles with null isAdult: {null_adult_titles}")

    null_start_year_titles = session.query(Title).filter(Title.startYear.is_(None)).count()
    logger.info(f"Titles with null startYear: {null_start_year_titles}")

    null_end_year_titles = session.query(Title).filter(Title.endYear.is_(None)).count()
    logger.info(f"Titles with null endYear: {null_end_year_titles}")

    null_runtime_titles = session.query(Title).filter(Title.runtimeMinutes.is_(None)).count()
    logger.info(f"Titles with null runtimeMinutes: {null_runtime_titles}")

    distinct_ids = session.query(Title.id).distinct().count()
    duplicate_ids = total_titles - distinct_ids
    logger.info(f"Duplicate title IDs: {duplicate_ids}")

    distinct_tconsts = session.query(Title.tconst).distinct().count()
    duplicate_tconsts = total_titles - distinct_tconsts
    logger.info(f"Duplicate tconsts: {duplicate_tconsts}")

    invalid_start_year_titles = (
        session.query(Title)
        .filter((Title.startYear < 1800) | (Title.startYear > date.today().year))
        .count()
    )
    logger.info(f"Titles with invalid startYear: {invalid_start_year_titles}")

    invalid_end_year_titles = (
        session.query(Title)
        .filter((Title.endYear < 1800) | (Title.endYear > date.today().year))
        .count()
    )
    logger.info(f"Titles with invalid endYear: {invalid_end_year_titles}")

    invalid_runtime_titles = (
        session.query(Title)
        .filter((Title.runtimeMinutes < 1) | (Title.runtimeMinutes > 500))
        .count()
    )
    logger.info(f"Titles with invalid runtimeMinutes: {invalid_runtime_titles}")

    logger.info("Title report complete.\n")

def report_genre_data(session: Session):
    logger.info("Running Genre report...")

    inconsistent_genre_names = (
        session.query(Genre)
        .filter(Genre.genre_name != func.initcap(Genre.genre_name))
        .count()
    )
    logger.info(f"Genres with inconsistent capitalization: {inconsistent_genre_names}")

    logger.info("Genre report complete.\n")

def report_title_genre_data(session: Session):
    logger.info("Running TitleGenre report...")

    total_title_genres = session.query(TitleGenre).count()
    logger.info(f"Total title-genre associations: {total_title_genres}")

    invalid_title_ids = (
        session.query(TitleGenre)
        .outerjoin(Title, TitleGenre.title_id == Title.id)
        .filter(Title.id.is_(None))
        .count()
    )
    logger.info(f"Title-genre associations with invalid title IDs: {invalid_title_ids}")

    invalid_genre_ids = (
        session.query(TitleGenre)
        .filter(~TitleGenre.genre_id.in_(session.query(Genre.id)))
        .count()
    )
    logger.info(f"Title-genre associations with invalid genre IDs: {invalid_genre_ids}")

    logger.info("TitleGenre report complete.\n")


def run_data_integrity_reports(session: Session):

    logger.info("Running data integrity reports...\n")

    report_title_data(session)
    report_genre_data(session)
    report_title_genre_data(session)

    logger.info("Data integrity reports complete.")