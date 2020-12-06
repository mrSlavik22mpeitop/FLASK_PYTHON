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
    price = Column(Integer)


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
    date_film = Column(String(250), nullable=False)
    price = Column(String(250), nullable=False)


class Seat(Base):
    __tablename__ = 'seat'
    id = Column(Integer, primary_key=True)
    row = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    branch_id = Column(Integer, nullable=False)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    second_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Reservation(Base):
     __tablename__ = "reservation"
     id = Column(Integer, primary_key=True)
     reserved = Column(Integer, nullable=False)
     user_id = Column(Integer, ForeignKey(User.id), nullable=False)
     paid = Column(Integer, nullable=False)



class Seat_Reserved(Base):
    __tablename__ = "seat_reserved"
    id = Column(Integer, primary_key=True)
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False)
    reservation_id = Column(Integer, ForeignKey(Reservation.id), nullable=False)
    screening_id = Column(Integer, ForeignKey(Screening.id), nullable=False)


class Autorization(Base):
    __tablename__ = "autorization"
    id = Column(Integer, primary_key=True)
    autorization_username = Column(String(250), nullable=False)
    autorization_password = Column(String(250), nullable=False)

engine = create_engine('sqlite:///cinema-collection.db')
Base.metadata.create_all(engine)
