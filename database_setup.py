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
    cast = Column(String(250))
    price = Column(String(250))

engine = create_engine('sqlite:///books-collection.db')
Base.metadata.create_all(engine)