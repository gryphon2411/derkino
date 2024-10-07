import uuid

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from postgresinit.postgres_commons import Base


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
    title_id = Column(UUID(as_uuid=True), ForeignKey('title.id'), primary_key=True, index=True)
    genre_id = Column(Integer, ForeignKey('genre.id'), primary_key=True, index=True)
