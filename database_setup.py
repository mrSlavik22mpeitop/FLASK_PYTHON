import sys
# для настройки баз данных
from sqlalchemy import Column, ForeignKey, Integer, String

# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base

# для создания отношений между таблицами
from sqlalchemy.orm import relationship

# для настроек
from sqlalchemy import create_engine

# создание экземпляра declarative_base
Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    genre = Column(String(250))
    price = Column(String(250))


class Branch(Base):
    __tablename__ = 'branch'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    seats = Column(Integer, nullable=False)

class Screening(Base):
    __tablename__ = 'screening'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)
    branch_id = Column(Integer, ForeignKey(Branch.id), nullable=False)
    screening_time = Column(String(250), nullable=False)


class Seat(Base):
    __tablename__ = 'seat'
    id = Column(Integer, primary_key=True)
    row = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    branch_id = Column(Integer, nullable=False)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(Integer, nullable=False)
    password = Column(Integer, nullable=False)

engine = create_engine('sqlite:///books-collection.db')
Base.metadata.create_all(engine)
