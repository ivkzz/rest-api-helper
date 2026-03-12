"""
Модуль настройки базы данных.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Генератор сессии базы данных.
    """
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()
