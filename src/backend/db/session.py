from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.backend.config import config
from src.backend.db.models.base import Base
from src.backend.db.models import user


engine = create_engine(
    f"mysql+pymysql://{config.MYSQL_USERNAME}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}?charset=utf8")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

Base.metadata.create_all(engine)

