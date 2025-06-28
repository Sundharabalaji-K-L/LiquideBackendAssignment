from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session, DeclarativeBase, sessionmaker
from app.config import settings


SQLALCHEMY_DATABASE_URL: str = f"mysql+pymysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal= sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db

    finally:
        db.close()

